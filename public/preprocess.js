// Image preprocessing: one client-side step per photo before it ever leaves
// the device. Per SPEC.md: fix EXIF rotation, downscale so the longest edge
// is at most 1568px, re-encode as JPEG, step quality down until the result
// fits the size budget, then base64 encode for transport.

const MAX_EDGE_PX = 1568;
const INITIAL_QUALITY = 0.8;
const QUALITY_STEPS = [0.8, 0.7, 0.6];
const MAX_BYTES = 1.2 * 1024 * 1024;

// createImageBitmap with imageOrientation: 'from-image' applies EXIF
// rotation for us on supporting browsers. Where it is not supported (older
// Safari), fall back to drawing through an offscreen canvas, which reads
// pixels in their already-rotated, on-screen orientation regardless of EXIF,
// achieving the same visual result by a different mechanism.
async function loadOrientedBitmap(file) {
  try {
    return await createImageBitmap(file, { imageOrientation: "from-image" });
  } catch {
    const url = URL.createObjectURL(file);
    try {
      const img = await new Promise((resolve, reject) => {
        const el = new Image();
        el.onload = () => resolve(el);
        el.onerror = reject;
        el.src = url;
      });
      const canvas = document.createElement("canvas");
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0);
      return await createImageBitmap(canvas);
    } finally {
      URL.revokeObjectURL(url);
    }
  }
}

function scaledDimensions(width, height) {
  const longestEdge = Math.max(width, height);
  if (longestEdge <= MAX_EDGE_PX) return { width, height };
  const scale = MAX_EDGE_PX / longestEdge;
  return {
    width: Math.round(width * scale),
    height: Math.round(height * scale),
  };
}

function canvasToBlob(canvas, quality) {
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error("toBlob failed"))),
      "image/jpeg",
      quality,
    );
  });
}

function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      // reader.result is a data URL ("data:image/jpeg;base64,...."); only
      // the payload after the comma is the base64 the API wants.
      const commaIndex = reader.result.indexOf(",");
      resolve(reader.result.slice(commaIndex + 1));
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

// Downscale, re-encode, and step quality down until the blob fits the size
// budget or the quality steps are exhausted (the last step's result is
// returned regardless, since a slightly oversized image is still better
// than none, and the worker's own 1.5MB body cap is the final backstop).
async function normalizeToJpeg(bitmap) {
  const { width, height } = scaledDimensions(bitmap.width, bitmap.height);
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(bitmap, 0, 0, width, height);

  let blob = await canvasToBlob(canvas, INITIAL_QUALITY);
  for (const quality of QUALITY_STEPS.slice(1)) {
    if (blob.size <= MAX_BYTES) break;
    blob = await canvasToBlob(canvas, quality);
  }
  return blob;
}

// Public entry point: File in, { media_type, data } out, ready to drop
// straight into an extraction request's image field.
export async function preprocessPhoto(file) {
  const bitmap = await loadOrientedBitmap(file);
  try {
    const blob = await normalizeToJpeg(bitmap);
    const data = await blobToBase64(blob);
    return { media_type: "image/jpeg", data };
  } finally {
    bitmap.close();
  }
}
