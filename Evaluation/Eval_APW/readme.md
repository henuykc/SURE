<h2>Evulation on AFP-APW</h2>
The script is based on a large-scale evaluation of relation extraction systems based on an automatic annotator. The details of the method are given in:

```
Mirko Bronzi, Zhaochen Guo, Filipe Mesquita, Denilson Barbosa, Paolo Merialdo, Automatic Evaluation of Relation Extraction Systems on Large-scale. In Proceedings of the Joint Workshop on Automatic Knowledge Base Construction and Web-scale Knowledge Extraction, AKBC-WEKEX 2012
```

and

```
Lin, W. H., Wu, Y. L., & Yu, L. C. (2012). Online computation of mutual information and word context entropy. International Journal of Future Computer and Communication, 1(2), 167.
```

<b>indexing.py</b>:

This script index the latest cleaned Wikipedia dumps.

<b>kb.py</b>

This script checks the data against the [DBpedia](https://wiki.dbpedia.org/) dataset. 

The sample 1k sentences from English Gigaword Collection, namely the AFP, APW are avialable inside the data folder.
