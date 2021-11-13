### Handling multiple matches

#### Overlapping:

    "abcabc", patterns=["abc","bca","cab"] [,allmatches=True]
    "abc"[,"abc"],"bca","cab"

#### Non-overlapping:

    "abcabc", patterns=["abc","bca","cab"] [, allmatches=True]
    "abc" [,"abc"]
