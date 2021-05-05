import stops from "./stops";

const boldify = (text: string, query: string) => {
  const lowerContains = (qList: string[], word: string) => {
    const depuncWord = word.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    const result = qList.map((qWord) => {
      const depuncQWord = qWord.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
      return (
        depuncQWord.toLowerCase() === depuncWord.toLowerCase() &&
        !stops.includes(depuncQWord) &&
        !stops.includes(depuncWord)
      );
    });
    return result.includes(true);
  };

  const tList = text.split(" ");
  const qList = query.split(" ");
  const bolded = tList.map((word) => {
    if (lowerContains(qList, word)) {
      return `<strong>${word}</strong>`;
    }
    return word;
  });
  return bolded.join(" ");
};

export default boldify;
