// Developed by Mehdi ORANUSS | Powered by Claude
// Builds the intro After Effects project from the data block D (written by build_intro_ai_aep.py, prepended above).
(function () {
    var LOG = [];
    function log(s) { LOG.push(s); }
    function flush() { var f = new File(D.files.log); f.encoding = "UTF-8"; f.open("w"); f.write(LOG.join("\n")); f.close(); }
    var INK = [0x1b / 255, 0x12 / 255, 0x40 / 255], WHITE = [1, 1, 1];
    var EASE = { inout3: [0, 65, 0, 65], inout2: [0, 45, 0, 45], expoOut: [6.25, 16, 0, 70], in3: [0, 32, 3.03, 33] };

    function dims(p) {
        var t = p.propertyValueType;
        if (t == PropertyValueType.TwoD_SPATIAL || t == PropertyValueType.ThreeD_SPATIAL || t == PropertyValueType.SHAPE || t == PropertyValueType.OneD) return 1;
        return p.value.length;
    }
    function speed(p, v1, v2, d, f) {
        if (f === 0) return 0;
        if (p.propertyValueType == PropertyValueType.OneD) return (v2 - v1) / d * f;
        var s = 0; for (var i = 0; i < v1.length; i++) s += (v2[i] - v1[i]) * (v2[i] - v1[i]);
        return Math.sqrt(s) / d * f;
    }
    // one tween = two keys with an eased curve between them (GSAP ease approximated with AE speed/influence)
    function seg(p, t1, v1, t2, v2, e) {
        p.setValueAtTime(t1, v1); p.setValueAtTime(t2, v2);
        var i1 = p.nearestKeyIndex(t1), i2 = p.nearestKeyIndex(t2), E = EASE[e], n = dims(p), a = [], b = [], k;
        for (k = 0; k < n; k++) {
            var dv = (n > 1) ? ((v2[k] === undefined || v1[k] === undefined) ? 0 : v2[k] - v1[k]) : 0;
            var so = (n > 1) ? dv / (t2 - t1) * E[0] : speed(p, v1, v2, t2 - t1, E[0]);
            var si = (n > 1) ? dv / (t2 - t1) * E[2] : speed(p, v1, v2, t2 - t1, E[2]);
            if (p.propertyValueType == PropertyValueType.SHAPE) { so = 0; si = 0; }
            a.push(new KeyframeEase(so, Math.max(0.1, E[1])));
            b.push(new KeyframeEase(si, Math.max(0.1, E[3])));
        }
        p.setTemporalEaseAtKey(i1, p.keyInTemporalEase(i1), a);
        p.setTemporalEaseAtKey(i2, b, p.keyOutTemporalEase(i2));
    }
    function rr(L, T, R, B, r) {                       // CSS inset(... round r) as an 8-vertex rounded rect
        r = Math.min(r, (R - L) / 2, (B - T) / 2); var k = 0.5523 * r, s = new Shape();
        s.vertices = [[L + r, T], [R - r, T], [R, T + r], [R, B - r], [R - r, B], [L + r, B], [L, B - r], [L, T + r]];
        s.inTangents = [[-k, 0], [0, 0], [0, -k], [0, 0], [k, 0], [0, 0], [0, k], [0, 0]];
        s.outTangents = [[0, 0], [k, 0], [0, 0], [0, k], [0, 0], [-k, 0], [0, 0], [0, -k]];
        s.closed = true; return s;
    }
    function camShape(v) { return rr(v[3], v[0], 1920 - v[1], 1080 - v[2], v[4]); }
    function camPos(v) { return [D.face[0] + v[5], D.face[1] + v[6]]; }
    function camScale(v) { return [v[7] * 100, v[7] * 100]; }
    function fx(layer, match) { return layer.property("ADBE Effect Parade").addProperty(match); }
    function hex(h) { return [parseInt(h.substr(1, 2), 16) / 255, parseInt(h.substr(3, 2), 16) / 255, parseInt(h.substr(5, 2), 16) / 255]; }
    function fmt(t) { var m = Math.floor(t / 60), s = (t - m * 60).toFixed(2); return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s; }

    try {
        app.beginSuppressDialogs();
        if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
        app.newProject();
        var P = app.project;
        function folder(n) { return P.items.addFolder(n); }
        var fMain = folder("00 Main"), fPre = folder("01 Precomps"), fKW = folder("02 Keywords (editable text)"), fPl = folder("03 Plates (rendered graphics)"),
            fCam = folder("04 Camera"), fAud = folder("05 Audio"), fSfx = folder("06 SFX (OrcaXV)"), fRef = folder("07 Reference");
        function imp(path, f) {
            var it = P.importFile(new ImportOptions(new File(path)));
            it.parentFolder = f;
            try { if (it.mainSource && it.hasVideo) it.mainSource.conformFrameRate = D.fps; } catch (e) {}
            return it;
        }
        var iBG = imp(D.files.bg, fPl), iGFX = imp(D.files.gfx, fPl), iTOP = imp(D.files.top, fPl);
        iGFX.mainSource.guessAlphaMode(); iTOP.mainSource.guessAlphaMode();
        var iCam = imp(D.files.aroll, fCam), iRaw = imp(D.files.raw, fCam), iVoice = imp(D.files.voice, fAud), iMix = imp(D.files.mix, fAud);
        var iRef = imp(D.files.ref, fRef);
        log("alpha gfx=" + iGFX.mainSource.alphaMode + " top=" + iTOP.mainSource.alphaMode + " hasAlpha=" + iGFX.mainSource.hasAlpha);

        var main = P.items.addComp("Intro-AI-Editing (main)", 1920, 1080, 1, D.dur, D.fps); main.parentFolder = fMain;
        main.bgColor = hex("#efe9ff");

        // ---- camera precomp: footage + punch-in zooms around the face ----
        var cz = P.items.addComp("CAM zoom (real footage + punch-ins)", 1920, 1080, 1, D.dur, D.fps); cz.parentFolder = fPre;
        var cl = cz.layers.add(iCam); cl.audioEnabled = false; cl.name = "Camera footage (tight cut)";
        cl.transform.anchorPoint.setValue(D.face); cl.transform.position.setValue(D.face);
        var zs = cl.transform.scale, z, j;
        for (j = 0; j < D.zoom.length - 1; j++) {
            if (D.zoom[j][2] == "a" && D.zoom[j + 1][2] == "b") {
                z = D.zoom[j]; var z2 = D.zoom[j + 1];
                seg(zs, z[0], [z[1][0] * 100, z[1][0] * 100], z2[0], [z2[1][0] * 100, z2[1][0] * 100], "inout2");
            }
        }

        // ---- bottom of the stack first (AE adds new layers on top) ----
        var ref = main.layers.add(iRef); ref.name = "REFERENCE approved FINAL-v2 (guide, off)"; ref.guideLayer = true; ref.enabled = false; ref.audioEnabled = false; ref.label = 0;
        var mix = main.layers.add(iMix); mix.name = "FINAL MIX voice+SFX (reference, off)"; mix.audioEnabled = false; mix.label = 0;
        for (j = D.sfx.length - 1; j >= 0; j--) {
            var s = D.sfx[j], it = null, q;
            for (q = 1; q <= fSfx.numItems; q++) if (fSfx.item(q).mainSource.file.fsName == new File(s.file).fsName) it = fSfx.item(q);
            if (!it) it = imp(s.file, fSfx);
            var L = main.layers.add(it);
            L.name = "SFX " + fmt(s.t) + "  " + s.id + " " + s.name;
            L.comment = s.note;
            L.startTime = s.start - s.skip; L.inPoint = s.start;
            var lv = L.property("ADBE Audio Group").property("ADBE Audio Levels");
            lv.setValue([s.gain, s.gain]);
            if (s.trim) { L.outPoint = Math.min(s.start + s.trim, D.dur); lv.setValueAtTime(L.outPoint - 0.25, [s.gain, s.gain]); lv.setValueAtTime(L.outPoint, [-48, -48]); }
            L.label = 11;
        }
        var voice = main.layers.add(iVoice); voice.name = "VOICE (polished)"; voice.label = 9;
        var bg = main.layers.add(iBG); bg.name = "BG plate (background world + split card)"; bg.label = 2;

        // ---- camera: real footage with the full / split / circle layouts ----
        var cam = main.layers.add(cz); cam.name = "Camera"; cam.label = 10;
        cam.transform.anchorPoint.setValue(D.face);
        var mk = cam.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); mk.name = "Layout";
        var mp = mk.property("ADBE Mask Shape");
        mp.setValue(camShape(D.cam[0][1])); cam.transform.position.setValue(camPos(D.cam[0][1])); cam.transform.scale.setValue(camScale(D.cam[0][1]));
        for (j = 0; j < D.cam.length - 1; j++) {
            if (D.cam[j][2] == "a" && D.cam[j + 1][2] == "b") {
                var a = D.cam[j], b = D.cam[j + 1];
                if (b[0] - a[0] < 0.02) { b = [a[0] + 0.034, b[1]]; }
                seg(mp, a[0], camShape(a[1]), b[0], camShape(b[1]), "inout3");
                seg(cam.transform.position, a[0], camPos(a[1]), b[0], camPos(b[1]), "inout3");
                seg(cam.transform.scale, a[0], camScale(a[1]), b[0], camScale(b[1]), "inout3");
            }
        }
        var raw = main.layers.add(iRaw); raw.name = "RAW opening (untouched take)"; raw.audioEnabled = false; raw.inPoint = 0; raw.outPoint = 3.12; raw.label = 10;
        var gfx = main.layers.add(iGFX); gfx.name = "GFX plate (scene graphics, alpha)"; gfx.label = 2;

        // ---- keywords: editable text precomps, entrance / exits as keyframes ----
        var nulls = {};
        for (j = 0; j < D.scenes.length; j++) {
            var sc = D.scenes[j];
            main.markerProperty.setValueAtTime(sc.start, new MarkerValue(sc.id));
            var hasKw = false; for (q = 0; q < D.kw.length; q++) if (D.kw[q].scene == sc.id) hasKw = true;
            if (!hasKw) continue;
            var nl = main.layers.addNull(D.dur); nl.name = "Scene " + sc.id + " exit (keyword parent)"; nl.label = 1;
            nl.transform.anchorPoint.setValue([50, 50]); nl.transform.position.setValue([960, 540]);
            nl.inPoint = sc.start; nl.outPoint = sc.end;
            if (sc.exit) {
                var e = sc.exit, t2 = e.t + e.d;
                if (e.kind == "left") seg(nl.transform.position, e.t, [960, 540], t2, [780, 540], "in3");
                if (e.kind == "up") seg(nl.transform.position, e.t, [960, 540], t2, [960, 420], "in3");
                if (e.kind == "blur") seg(nl.transform.scale, e.t, [100, 100], t2, [96.5, 96.5], "in3");
                if (e.kind == "zoom") seg(nl.transform.scale, e.t, [100, 100], t2, [125, 125], "in3");
            }
            nulls[sc.id] = nl;
        }
        function mkText(comp, str, ar, fs) {
            var T = comp.layers.addText(str), tp = T.property("ADBE Text Properties").property("ADBE Text Document"), d = tp.value;
            d.resetCharStyle(); d.resetParagraphStyle();
            d.font = ar ? "GraphikArabic-Bold" : "Poppins-ExtraBold"; d.fontSize = fs;
            d.applyFill = true; d.fillColor = INK; d.applyStroke = false; d.tracking = ar ? 0 : -10;
            d.justification = ParagraphJustification.LEFT_JUSTIFY;
            if (ar) { try { d.direction = ParagraphDirection.DIRECTION_RIGHT_TO_LEFT; } catch (e1) {} }
            tp.setValue(d);
            return T;
        }
        function glow(T, grad) {
            var ds = fx(T, "ADBE Drop Shadow");
            ds.property(1).setValue(WHITE); ds.property(2).setValue(grad ? 217 : 230); ds.property(3).setValue(180);
            ds.property(4).setValue(grad ? 8 : 6); ds.property(5).setValue(grad ? 20 : 30);
        }
        function gradient(T) {                          // .grad: 135deg #b69cff -> #7c3aed -> #4c1d95, through the glyphs only
            var g = fx(T, "ADBE Ramp");
            g.property(1).expression = "var r=thisLayer.sourceRectAtTime(time,false);[r.left,r.top]";
            g.property(2).setValue(hex("#a98bfb"));
            g.property(3).expression = "var r=thisLayer.sourceRectAtTime(time,false);[r.left+r.width,r.top+r.height]";
            g.property(4).setValue(hex("#4c1d95"));
            var sm = fx(T, "ADBE Set Matte3");
            sm.property(1).setValue(T.index);
            sm.property(2).setValue(4);                   // use the layer's own alpha (glyphs)
        }
        var kn = 0;
        for (j = D.kw.length - 1; j >= 0; j--) {
            var k = D.kw[j]; kn++;
            var kc = P.items.addComp("KW " + k.id + "  " + k.text, 1920, 1080, 1, D.dur, D.fps); kc.parentFolder = fKW;
            var full = mkText(kc, k.text, k.ar, k.fs), fr = full.sourceRectAtTime(0, false);
            var baseY = k.cy - (fr.top + fr.height / 2);
            var mixed = false; for (q = 1; q < k.spans.length; q++) if (k.spans[q][1] != k.spans[0][1]) mixed = true;
            if (!mixed) {
                full.name = k.text;
                full.transform.position.setValue([k.cx - (fr.left + fr.width / 2), baseY]);
                if (k.spans[0][1]) gradient(full);
                glow(full, k.spans[0][1]);
            } else {
                full.remove();
                var parts = [], tot = 0, gap = k.fs * 0.26;
                for (q = 0; q < k.spans.length; q++) {
                    var T = mkText(kc, k.spans[q][0], k.ar, k.fs), r = T.sourceRectAtTime(0, false);
                    T.name = k.spans[q][0] + (k.spans[q][1] ? " (gradient)" : "");
                    parts.push([T, r, k.spans[q][1]]); tot += r.width;
                }
                tot += gap * (parts.length - 1);
                var x = k.cx - tot / 2, order = [];
                for (q = 0; q < parts.length; q++) order.push(k.ar ? parts[parts.length - 1 - q] : parts[q]);
                for (q = 0; q < order.length; q++) {
                    order[q][0].transform.position.setValue([x - order[q][1].left, baseY]);
                    x += order[q][1].width + gap;
                    if (order[q][2]) gradient(order[q][0]);
                    glow(order[q][0], order[q][2]);
                }
            }
            var KL = main.layers.add(kc); KL.name = "KW  " + k.text; KL.label = 14;
            KL.transform.anchorPoint.setValue([k.cx, k.cy]); KL.transform.position.setValue([k.cx, k.cy]);
            KL.inPoint = k.tin; KL.outPoint = k.end;
            var bl = fx(KL, "ADBE Gaussian Blur 2");
            var tin = k.tin, te = tin + 0.32;
            seg(KL.transform.scale, tin, [135, 135], te, [100, 100], "expoOut");
            seg(KL.transform.opacity, tin, 0, te, 100, "expoOut");
            seg(bl.property(1), tin, 24, te, 0, "expoOut");
            var ex = k.out, scx = null; for (q = 0; q < D.scenes.length; q++) if (D.scenes[q].id == k.scene) scx = D.scenes[q].exit;
            if (!ex && scx) ex = { t: scx.t, d: scx.d, blur: scx.blur };
            if (ex) { seg(KL.transform.opacity, ex.t, 100, ex.t + ex.d, 0, "in3"); seg(bl.property(1), ex.t, 0, ex.t + ex.d, ex.blur * 1.5, "in3"); }
            if (nulls[k.scene]) KL.parent = nulls[k.scene];
        }
        log("keywords " + kn);

        // ---- camera copy drawn above the graphics during the circle beats ----
        var co = main.layers.add(cz); co.name = "Camera circle (on top, follows Camera)"; co.label = 10;
        co.transform.anchorPoint.expression = 'thisComp.layer("Camera").transform.anchorPoint';
        co.transform.position.expression = 'thisComp.layer("Camera").transform.position';
        co.transform.scale.expression = 'thisComp.layer("Camera").transform.scale';
        var mk2 = co.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); mk2.name = "Layout";
        mk2.property("ADBE Mask Shape").expression = 'thisComp.layer("Camera").mask("Layout").maskPath';
        var op = co.transform.opacity; op.setValueAtTime(0, 0);
        for (j = 0; j < D.over.length; j++) { op.setValueAtTime(D.over[j][0], 100); op.setValueAtTime(D.over[j][1], 0); }
        for (j = 1; j <= op.numKeys; j++) op.setInterpolationTypeAtKey(j, KeyframeInterpolationType.HOLD);
        var top = main.layers.add(iTOP); top.name = "TOP plate (circle ring + purple wipes)"; top.label = 2;

        P.save(new File(D.files.aep));
        main.openInViewer();
        log("saved " + D.files.aep + " layers=" + main.numLayers);
        app.endSuppressDialogs(false);
        log("OK");
    } catch (err) {
        log("ERROR line " + err.line + ": " + err.toString());
        try { app.endSuppressDialogs(false); } catch (e9) {}
    }
    flush();
})();
