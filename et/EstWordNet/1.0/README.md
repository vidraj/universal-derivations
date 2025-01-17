# Summary

Universal Derivations version of derivational relations extracted from EstWordNet, Estonian WordNet (https://www.cl.ut.ee/ressursid/teksaurus/).


# Introduction

Estonian Wordnet is based on the wordnet theory, and it has closely followed the principles adopted in the (English) Princeton WordNet and EuroWordNet projects. EstWordNet includes nouns, verbs, adjectives and adverbs, as well as a set of multiword units. Using automatic methods, Kahusk et al. (2010) enriched EstWordNet with some derivational relations that connect some lexemes into derivational families.

EstWordNet has been harmonized manually.


# Acknowledgments

We wish to thank all the developers and annotators of EstWordNet, including Kadri Kerner, Heili Orav, Sirli Parm, Neeme Kahusk, Kadri Vider, Kadri Vare, Liisi Pool, Lauri Eesmaa, Piia Taremaa, Maria Reile, Katrin Alekand, Ingmar Jaska, Helen Türk, Eleri Aedma, Ahti Lohk, Riin Kirt, Andrus Karjus, Marju Taukar, Kaisa Hunt, Nele Salveste, Olga-Anniki Villem, and Maarja-Liisa Pilvik.


## References

As a citation for the resource in articles, please use this:

* Kerner, Kadri; Orav, Heili; and Parm, Sirli. 2010. Growth and Revision of Estonian WordNet. Principles, Construction and Application of Multilingual WordNets. Narosa Publishing House, pages 198–202. http://www.cfilt.iitb.ac.in/gwc2010/pdfs/39_Estonian_WordNet__Kerner.pdf.
* Kahusk, Neeme; Kerner, Kadri; and Vider, Kadri. 2010. Enriching Estonian WordNet with Derivations and Semantic Relations. In Baltic hlt, pages 195–200. 

```
@ARTICLE{EstWordNet,
    title   = {{Growth and revision of Estonian wordnet}},
    author  = {Kerner, Kadri and Orav, Heili and Parm, Sirli},
    journal = {{Principles, Construction and Application of Multilingual Wordnets}},
    pages   = {198--202},
    year    = {2010},
    url     = {http://www.cfilt.iitb.ac.in/gwc2010/pdfs/39_Estonian_WordNet__Kerner.pdf}
}

@INPROCEEDINGS{EstWordNetDerivations,
    title       = {{Enriching Estonian WordNet with Derivations and Semantic Relations}},
    author      = {Kahusk, Neeme and Kerner, Kadri and Vider, Kadri},
    booktitle   = {Baltic hlt},
    pages       = {195--200},
    year        = {2010}
}
```


# License

The resource is licensed under the Creative Commons Attribution-ShareAlike 3.0 License (CC BY-SA 3.0).
License text is available in the file `LICENSE.txt`.


# Changelog

* 2020-05 UDer v1.0
    * Replacing LEMIDs to IDs in the tenth JSON-encoded column.
* 2019-09 UDer v0.5
    * Including EstWordNet v2.1 to the UDer collection.
    * Manual harmonization.


<pre>
=== Machine-readable metadata =================================================
Resource: EstWordNet
Language: Estonian
Authors: Kahusk, Neeme; Vider, Kadri; Kerner, Kadri; Orav, Heili; Parm, Sirli
License: CC BY-SA 3.0
Contact: https://www.cl.ut.ee/ressursid/teksaurus/
===============================================================================
</pre>

<pre>
=== Machine-readable metadata =================================================
Harmonized resource: EstWordNet
Harmonized version: 2.1
Data source: https://gitlab.keeleressursid.ee/avalik/data/raw/master/estwn/estwn-et-2.1.0.wip.xml
Data available since: UDer v0.5
Harmonization: manual
Common features: none
JSON features: was_in_family_with; other_parents
