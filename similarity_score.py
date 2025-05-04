from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


n = int(input("Enter number of documents: "))
documents = []
for i in range(n):
    doc = input(f"Enter document {i+1}: ")
    documents.append(doc)


vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)


cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()


print("\nSimilarity with Document 1:")
for i, score in enumerate(cosine_similarities, start=2):
    print(f"Document {i}: {score * 100:.2f}%")


if cosine_similarities.size > 0:
    most_similar_index = cosine_similarities.argmax() + 2
    print(f"\nMost similar document to Document 1 is Document {most_similar_index}")
    print(f"Similarity Score: {cosine_similarities.max() * 100:.2f}%")
else:
    print("\nNot enough documents to compare.")
