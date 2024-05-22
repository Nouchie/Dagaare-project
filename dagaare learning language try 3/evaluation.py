from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def compute_bleu(reference, candidate):
    reference = [reference.split()]
    candidate = candidate.split()
    smoothie = SmoothingFunction().method4
    score = sentence_bleu(reference, candidate, smoothing_function=smoothie)
    return score

# Example usage
reference_sentence = "What is your name?"
candidate_sentence = translate("What is your name?", max_sequence_length=100)
bleu_score = compute_bleu(reference_sentence, candidate_sentence)
print(f"BLEU Score: {bleu_score:.2f}")






from rouge import Rouge

def compute_rouge(reference, candidate):
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)
    return scores

# Example usage
reference_sentence = "What is your name?"
candidate_sentence = translate("What is your name?", max_sequence_length=100)
rouge_scores = compute_rouge(reference_sentence, candidate_sentence)
print(f"ROUGE Scores: {rouge_scores}")





def batch_evaluate(sentences, references, max_sequence_length=100):
    scores = []
    for eng_sentence, ref_sentence in zip(sentences, references):
        candidate_sentence = translate(eng_sentence, max_sequence_length)
        score = compute_bleu(ref_sentence, candidate_sentence)
        scores.append(score)
    return sum(scores) / len(scores)

# Example usage
sentences = ["What is your name?", "How are you?", "Where do you live?"]
references = ["What is your name?", "How are you?", "Where do you live?"]
average_bleu = batch_evaluate(sentences, references)
print(f"Average BLEU Score: {average_bleu:.2f}")
