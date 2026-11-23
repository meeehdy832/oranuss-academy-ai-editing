// Drop-in Root for a fresh Remotion project (src/Root.tsx). Registers the two examples from this skill.
// New compositions you build go in src/compositions/<Name>.tsx and get registered here the same way.
import React from "react";
import { Composition } from "remotion";
import { ProDemo, PRO_DEMO_DURATION } from "./examples/ProDemo";
import { TextLab, TEXT_LAB_DURATION } from "./examples/TextLab";

export const RemotionRoot: React.FC = () => (
  <>
    {/* The gold reel. mb = motion-blur samples: 1 for fast drafts, 10 for the final. */}
    <Composition id="ProDemo" component={ProDemo} durationInFrames={PRO_DEMO_DURATION} fps={30} width={1080} height={1080}
      defaultProps={{ mb: 10 }} />
    {/* Every text / pixel technique, one after another. */}
    <Composition id="TextLab" component={TextLab} durationInFrames={TEXT_LAB_DURATION} fps={30} width={1080} height={1080} />
  </>
);
