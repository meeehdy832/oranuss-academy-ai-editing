// Developed by Mehdi ORANUSS | Powered by Claude
// usage: face-track <in.mov> <out.json> [step_seconds]
// Detects the largest face every step seconds with macOS Vision and writes
// [{"t":..,"x":..,"y":..,"w":..,"h":..}] in pixels of the displayed (rotated) frame, origin top-left.
import AVFoundation
import Vision
import Foundation

let args = CommandLine.arguments
guard args.count >= 3 else { print("usage: face-track <in.mov> <out.json> [step]"); exit(2) }
let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let step = args.count > 3 ? Double(args[3])! : 0.5
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
let dur = CMTimeGetSeconds(asset.duration)
var out: [[String: Double]] = []
var t = 0.0
while t < dur {
    if let cg = try? gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil) {
        let W = Double(cg.width), H = Double(cg.height)
        let req = VNDetectFaceRectanglesRequest()
        try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
        if let f = (req.results ?? []).max(by: { $0.boundingBox.width * $0.boundingBox.height < $1.boundingBox.width * $1.boundingBox.height }) {
            let b = f.boundingBox
            out.append(["t": t, "x": b.minX * W, "y": (1 - b.maxY) * H, "w": b.width * W, "h": b.height * H, "W": W, "H": H])
        } else {
            out.append(["t": t, "x": -1, "y": -1, "w": 0, "h": 0, "W": W, "H": H])
        }
    }
    t += step
}
let data = try! JSONSerialization.data(withJSONObject: out, options: [])
try! data.write(to: URL(fileURLWithPath: args[2]))
print("frames", out.count)
