import Foundation
import PDFKit
import Vision
import AppKit

let pdfURL = URL(fileURLWithPath: "/Users/mercedes/.openclaw/workspace/tmp/seoulfuture/seoulfuture365.pdf")
guard let doc = PDFDocument(url: pdfURL) else { fatalError("Failed to open PDF") }
let maxPages = min(20, doc.pageCount)
print("PAGE_COUNT=\(doc.pageCount)")

func ocrPage(_ page: PDFPage) -> String {
    let pageRect = page.bounds(for: .mediaBox)
    let scale: CGFloat = 2.0
    let width = Int(pageRect.width * scale)
    let height = Int(pageRect.height * scale)
    guard width > 0, height > 0 else { return "" }
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    guard let ctx = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: 0, space: colorSpace, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return "" }
    ctx.setFillColor(NSColor.white.cgColor)
    ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
    ctx.saveGState()
    ctx.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: ctx)
    ctx.restoreGState()
    guard let image = ctx.makeImage() else { return "" }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = ["ko-KR", "en-US"]
    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    do { try handler.perform([request]) } catch { return "" }
    let obs = request.results ?? []
    return obs.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
}

for i in 0..<maxPages {
    guard let page = doc.page(at: i) else { continue }
    let txt = ocrPage(page)
    print("--- PAGE \(i+1) ---")
    print(txt.prefix(2500))
}
