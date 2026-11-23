import AVFoundation
import CoreImage
import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

// Seeded version of the video-editor-skill cutout-video tool (macOS Vision foreground-instance mask).
// Keeps only the instances found under the seed points, so a person printed on a poster behind the
// speaker is dropped while the speaker and what they hold (mic) stay.
// usage: cutout-seed <in.mov> <outMaskDir> <x,y> [<x,y> ...]   (seeds normalised 0-1, origin top-left)
let args = CommandLine.arguments
guard args.count >= 4 else { print("usage: cutout-seed <in.mov> <outMaskDir> <x,y> [<x,y> ...]"); exit(2) }
let inURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
let seeds: [(Double, Double)] = args[3...].map { s in
  let p = s.split(separator: ",").map { Double($0)! }
  return (p[0], p[1])
}
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

let asset = AVURLAsset(url: inURL)
let sem = DispatchSemaphore(value: 0)
var track: AVAssetTrack?
Task { track = try? await asset.loadTracks(withMediaType: .video).first; sem.signal() }
sem.wait()
guard let videoTrack = track else { print("no video track"); exit(1) }
let reader = try AVAssetReader(asset: asset)
let output = AVAssetReaderTrackOutput(track: videoTrack, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
output.alwaysCopiesSampleData = false
reader.add(output)
reader.startReading()

func labelsAtSeeds(_ buf: CVPixelBuffer) -> IndexSet {
  CVPixelBufferLockBaseAddress(buf, .readOnly)
  defer { CVPixelBufferUnlockBaseAddress(buf, .readOnly) }
  let w = CVPixelBufferGetWidth(buf), h = CVPixelBufferGetHeight(buf)
  let row = CVPixelBufferGetBytesPerRow(buf)
  let base = CVPixelBufferGetBaseAddress(buf)!.assumingMemoryBound(to: UInt8.self)
  var out = IndexSet()
  for (sx, sy) in seeds {
    let x = min(w - 1, max(0, Int(sx * Double(w)))), y = min(h - 1, max(0, Int(sy * Double(h))))
    let v = Int(base[y * row + x])
    if v > 0 { out.insert(v) }
  }
  return out
}

let ctx = CIContext()
let gray = CGColorSpaceCreateDeviceGray()
var n = 0, empty = 0, fallback = 0
var lastKeep = IndexSet()
let t0 = Date()
while let sample = output.copyNextSampleBuffer(), let pb = CMSampleBufferGetImageBuffer(sample) {
  n += 1
  let handler = VNImageRequestHandler(cvPixelBuffer: pb)
  let req = VNGenerateForegroundInstanceMaskRequest()
  var maskImage: CIImage
  do {
    try handler.perform([req])
    if let obs = req.results?.first {
      var keep = labelsAtSeeds(obs.instanceMask).intersection(obs.allInstances)
      if keep.isEmpty {                       // seed missed this frame: reuse last frame's labels, else everything
        fallback += 1
        keep = lastKeep.intersection(obs.allInstances)
        if keep.isEmpty { keep = obs.allInstances }
      }
      lastKeep = keep
      let m = try obs.generateScaledMaskForImage(forInstances: keep, from: handler)
      maskImage = CIImage(cvPixelBuffer: m)
    } else {
      empty += 1
      maskImage = CIImage(color: .black).cropped(to: CGRect(x: 0, y: 0, width: CVPixelBufferGetWidth(pb), height: CVPixelBufferGetHeight(pb)))
    }
  } catch { print("frame \(n): \(error)"); exit(1) }
  guard let cg = ctx.createCGImage(maskImage, from: maskImage.extent, format: .L8, colorSpace: gray) else { exit(1) }
  let url = outDir.appendingPathComponent(String(format: "%05d.png", n))
  let dest = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(dest, cg, nil)
  CGImageDestinationFinalize(dest)
  if n % 300 == 0 { print("\(n) frames, \(String(format: "%.3f", Date().timeIntervalSince(t0) / Double(n)))s/frame") }
}
print("done: \(n) frames (\(empty) empty, \(fallback) seed misses) in \(String(format: "%.1f", Date().timeIntervalSince(t0)))s")
