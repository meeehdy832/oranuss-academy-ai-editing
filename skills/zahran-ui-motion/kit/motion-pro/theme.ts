// THEME: the fonts the kit and the examples use. Loaded through @remotion/google-fonts, so they render the same on
// every machine (no system-font fallback). Swap or add families here; call `useFontsReady()` in your composition.
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

const inter = loadInter("normal", { weights: ["300", "400", "500", "600", "700"], subsets: ["latin"] });

export const FONT = {
  /** Apple-like UI text and headlines (SF Pro stand-in). */
  ui: inter.fontFamily,
  mono: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
} as const;
