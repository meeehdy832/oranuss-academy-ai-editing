// Beat schema shared by ExplainerDoc.tsx (one beat = one scene, times in seconds).
export type Item = { icon?: string; label: string; sub?: string };
export type Beat = {
  from: number; to: number;
  type: "title" | "icons" | "steps" | "stat" | "vs" | "image" | "cutout" | "quote" | "video" | "flow" | "equation" | "bars" | "chain";
  title?: string; sub?: string; icon?: string; items?: Item[];
  value?: number; prefix?: string; suffix?: string;
  left?: Item; right?: Item; img?: string; accent?: string;
};
