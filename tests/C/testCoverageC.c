// testConverageC.c

// cd to tests/C
// First, run: gcc coverageC.c testCoverageC.c -o testCoverage 
// Then, run: ./testCoverage 

#include <stdio.h>

// from coverageC.c
void checkCoverageDetailed(const char *transcript,
                           const char *questions[], int qlen, double threshold,
                           double scores_out[], int asked_flags[],
                           int *askedCount, int *missedCount, double *coverage_out);

static int run_case(const char *name, const char *label, const char *transcript,
                    const char *questions[], int qlen, double threshold,
                    int expectAsked, double expectCoverage) {
    double scores[64];
    int asked_flags[64];
    int asked = 0, missed = 0;
    double coverage = 0.0;

    printf("\n===== CASE: %s =====\n", name);
    printf("--- Transcript (%s) ---\n%s\n---------------------------------------\n", label, transcript);

    checkCoverageDetailed(transcript, questions, qlen, threshold,
                          scores, asked_flags, &asked, &missed, &coverage);

    // Detailed results
    printf("  asked:\n");
    for (int i = 0; i < qlen; i++) {
        if (asked_flags[i]) {
            printf("    - %s (score=%.2f)\n", questions[i], scores[i]);
        }
    }
    printf("  missed:\n");
    for (int i = 0; i < qlen; i++) {
        if (!asked_flags[i]) {
            printf("    - %s (score=%.2f)\n", questions[i], scores[i]);
        }
    }
    printf("  coverage=%.2f\n", coverage);

    // PASS/FAIL for this case
    int pass = (asked == expectAsked) && ( (coverage - expectCoverage < 1e-9) && (expectCoverage - coverage < 1e-9) );
    printf("[%s] %s\n", pass ? "PASS" : "FAIL", name);
    return pass ? 1 : 0;
}

int main(void) {
    const char *questions[] = {
        "What is the address of the emergency?",
        "Is anyone injured?",
        "What is your callback number?"
    };
    const int qlen = 3;
    const double threshold = 0.6;

    const char *positiveTranscript =
        "This is 911. What’s the address of the emergency today? "
        "Is anyone injured there? I also need your callback number please.";

    const char *negativeTranscript =
        "This is 911. Tell me what happened.";

    int total = 0, ok = 0;

    total++; ok += run_case("All detected", "positive", positiveTranscript, questions, qlen, threshold, 3, 1.0);
    total++; ok += run_case("None detected", "negative", negativeTranscript, questions, qlen, threshold, 0, 0.0);

    printf("\nRESULT: %d/%d tests passed.\n", ok, total);
    return (ok == total) ? 0 : 1;
}
