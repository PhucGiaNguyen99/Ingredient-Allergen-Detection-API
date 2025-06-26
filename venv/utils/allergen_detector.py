import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

def detect_allergens_spacy(text, allergen_list):
    # Process the input text
    doc = nlp(text)
    detected = set()

    # Implement PhraseMatcher for detecting exact phrases
    # Create a PhraseMatcher with case-insensitive matching (LOWER)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    # Convert each allergen string into a spaCy Doc object for matching
    patterns = [nlp.make_doc(allergen) for allergen in allergen_list]

    # Add these patterns to the matcher under the label "ALLERGENS"
    matcher.add("ALLERGENS", patterns)

    # Run the matcher against the input doc
    matches = matcher(doc)

    # Extract and store matched phrases from the doc
    for match_id, start, end in matches:
        detected.add(doc[start:end].text.lower())

    # Implement Token-level similarity (fuzzy match) to detect tokens that are semantically close to allergens
    # Preprocess allergen list as spaCy Doc objects for similarity comparison
    allergen_docs = [nlp(allergen) for allergen in allergen_list]

    # Loop over each token in the ingredient text
    for token in doc:
        # Compare the token with each allergen for similarity
        for allergen_doc in allergen_docs:
            # If similarity is reasonably high, consider it a match
            if token.similarity(allergen_doc) > 0.75:
                detected.add(allergen_doc.text.lower())

    # Implement Lemmatized token match to match lemmatized forms of tokens
    # Create a set of lemmatized, lowercase words from the input text
    lemmas = set(token.lemma_.lower() for token in doc if token.is_alpha)
    for allergen in allergen_list:
        if allergen.lower() in lemmas:
            detected.add(allergen.lower())

    # Implement Named Entity Recognition (NER) to detect allergens identified as named entities
    # Focus on food-related or product-related entity labels
    for ent in doc.ents:
        if ent.label_ in ["FOOD", "ORG", "PRODUCT"]:
            if ent.text.lower() in allergen_list:
                detected.add(ent.text.lower())

    return list(detected)