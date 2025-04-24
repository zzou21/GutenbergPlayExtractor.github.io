import spacy, json

def usingUnprocessedTXT(input):
    txtFile = open(input, "r")
    txtContent = txtFile.read()
    txtFile.close()

    nlp = spacy.load("en_core_web_sm")
    beginningIndex = txtContent.index("Dramatis Personæ") + len("Dramatis Personæ")
    endIndex = txtContent.index("*** END OF THE PROJECT GUTENBERG EBOOK AS YOU LIKE IT ***")
    cleanedContent = txtContent[beginningIndex:endIndex]
    cleanedContent = " ".join([sentence.strip() for sentence in cleanedContent.split("\n") if sentence.strip()])
    analysis = nlp(cleanedContent)

    entityDictionary = {}

    for entity in analysis.ents:
        label = entity.label_
        text = entity.text
        if label not in entityDictionary:
            entityDictionary[label] = [text]
        else:
            entityDictionary[label].append(text)

    return entityDictionary

def usingProcessedJson(input):
    with open(input, "r") as jsonFile:
        textContent = json.load(jsonFile)

    entityDictionary = {}
    nlp = spacy.load("en_core_web_sm")
    for name, dialogues in textContent.items():
        textContent[name] = " ".join(dialogues)
    for name, dialogues in textContent.items():
        analysisPerPerson = nlp(dialogues)
        entityDictionary[name] = {}
        for entity in analysisPerPerson.ents:
            label = entity.label_
            text = entity.text
            if label in ["PERSON", "ORG", "GPE", "LOC", "PRODUCT"]:
                if label not in entityDictionary[name]:
                    entityDictionary[name][label] = [text]
                else:
                    entityDictionary[name][label].append(text)

    return entityDictionary

if __name__ == "__main__":
    unprocessedTXTFile = "/Users/Jerry/Desktop/GutenbergPlayExtractor.github.io/OriginalCode/practiceTXT/pg1523.txt"
    processedJsonFile = "/Users/Jerry/Desktop/GutenbergPlayExtractor.github.io/OriginalCode/jsonStorage/AsYouLikeIt.json"
    # TXTOutputDict = usingUnprocessedTXT(unprocessedTXTFile)
    # for entity, content in TXTOutputDict.items():
    #     print(entity, ": ", content, "\n")
    jsonOutputDict = usingProcessedJson(processedJsonFile)
    for name, entityDict in jsonOutputDict.items():
        print(name, ": ", entityDict, "\n")