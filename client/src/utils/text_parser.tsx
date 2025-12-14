export const parseCitations = (text: string) => {
  const parts = [];
  //  regex to match both single [^1] and multiple [^2, ^3] citations
  const regex = /\[\^(\d+(?:,\s*\^\d+)*)\]/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    // Push normal text before citation
    if (match.index > lastIndex) {
      parts.push({
        type: "text",
        content: text.substring(lastIndex, match.index),
        key: `text-${lastIndex}`,
      });
    }

    // Extract all citation numbers from the match
    // Handle formats like "1" or "2, ^3" or "9, ^10"
    const citationNumbers = match[1]
      .split(",")
      .map((num) => parseInt(num.trim().replace("^", ""), 10));

    // Push clickable citation
    parts.push({
      type: "citation",
      numbers: citationNumbers,
      rawMatch: match[1],
      key: `cite-${match.index}`,
    });

    lastIndex = match.index + match[0].length;
  }

  // Push remaining text after last citation
  if (lastIndex < text.length) {
    parts.push({
      type: "text",
      content: text.substring(lastIndex),
      key: `text-${lastIndex}`,
    });
  }
  return parts;
};
