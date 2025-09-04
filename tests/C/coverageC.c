// coverageC.c

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_TOKENS 256
#define MAX_LEN 1024

// Small stopword list
static const char *STOPWORDS[] = {
    "a","an","the","is","are","of","to","your","my","our","their","his","her","there","this","that","what"
};
static const int STOPCOUNT = 17;

// normalize: lowercase ASCII, strip punctuation, split by whitespace, drop stopwords.
// Returns number of tokens written to `tokens`.
static int normalize(const char *text, char tokens[MAX_TOKENS][MAX_LEN]) {
    char buf[MAX_LEN * 2];
    size_t i = 0, j = 0;
    int count = 0;

    // Lowercase ASCII, replace non-alnum with space
    while (text[i] && j < sizeof(buf) - 1) {
        unsigned char uc = (unsigned char)text[i];
        int lc = tolower(uc);
        if (isalnum(uc) || isspace(uc)) {
            buf[j++] = (char)lc;
        } else {
            buf[j++] = ' ';
        }
        i++;
    }
    buf[j] = '\0';

    // Tokenize by whitespace
    char *saveptr = NULL;
    char *tok = strtok_r(buf, " \t\r\n", &saveptr);
    while (tok && count < MAX_TOKENS) {
        // stopword check
        int skip = 0;
        for (int s = 0; s < STOPCOUNT; s++) {
            if (strcmp(tok, STOPWORDS[s]) == 0) { skip = 1; break; }
        }
        if (!skip) {
            strncpy(tokens[count], tok, MAX_LEN - 1);
            tokens[count][MAX_LEN - 1] = '\0';
            count++;
        }
        tok = strtok_r(NULL, " \t\r\n", &saveptr);
    }
    return count;
}

// Compute token-overlap score between a question and the transcript
static double tokenOverlapScore(const char *question, const char *transcript) {
    char qtokens[MAX_TOKENS][MAX_LEN];
    char ttokens[MAX_TOKENS][MAX_LEN];
    int qcount = normalize(question, qtokens);
    int tcount = normalize(transcript, ttokens);

    if (qcount == 0) return 0.0;

    int overlap = 0;
    for (int i = 0; i < qcount; i++) {
        for (int j = 0; j < tcount; j++) {
            if (strcmp(qtokens[i], ttokens[j]) == 0) {
                overlap++;
                break;
            }
        }
    }
    return (double)overlap / (double)qcount;
}

/**
 * Detailed coverage:
 *  - scores_out[i]  : score for questions[i]
 *  - asked_flags[i] : 1 if asked (score >= threshold), else 0
 *  - askedCount / missedCount / *coverage_out set
 */
void checkCoverageDetailed(const char *transcript,
                           const char *questions[], int qlen, double threshold,
                           double scores_out[], int asked_flags[],
                           int *askedCount, int *missedCount, double *coverage_out) {
    int a = 0, m = 0;
    for (int i = 0; i < qlen; i++) {
        double score = tokenOverlapScore(questions[i], transcript);
        // round to 2 decimals for nicer output parity with other langs
        scores_out[i] = ((double)((int)(score * 100 + 0.5))) / 100.0;
        if (score >= threshold) { asked_flags[i] = 1; a++; }
        else { asked_flags[i] = 0; m++; }
    }
    *askedCount = a;
    *missedCount = m;
    *coverage_out = qlen > 0 ? ((double)a / (double)qlen) : 0.0;
}
