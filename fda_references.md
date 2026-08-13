# References

Numbered reference list (Vancouver style). Cited inline throughout the project using the bracketed number. Every source below was individually re-verified (URL, DOI, and claimed content checked against the actual source) as of August 2026.

1. U.S. Food and Drug Administration. FDA Adverse Event Reporting System (FAERS) Database. https://www.fda.gov/drugs/drug-approvals-and-databases/fda-adverse-event-reporting-system-faers-database

2. openFDA. FDA Adverse Event Reporting System dataset documentation. https://open.fda.gov/data/faers

3. Sakaeda T, Tamon A, Kadoyama K, Okuno Y. (2013). Data Mining of the Public Version of the FDA Adverse Event Reporting System. *International Journal of Medical Sciences*, 10(7), 796-803. https://www.medsci.org/v10p0796.htm (DOI: 10.7150/ijms.6048)

4. Hoffman KB, Demakas AR, Dimbil M, et al. (2014). Stimulated reporting: the impact of US Food and Drug Administration-issued alerts on the adverse event reporting system (FAERS). *Drug Safety*, 37, 971-980. https://link.springer.com/article/10.1007/s40264-014-0225-0

5. BRASH syndrome as a clinical syndrome driven by polypharmacy: a pharmacovigilance study of 1,081 cases from FAERS. *medRxiv* (preprint, not yet peer reviewed). https://www.medrxiv.org/content/10.64898/2026.01.15.26344203v1

6. U.S. Food and Drug Administration. FDA Adverse Event Monitoring System (AEMS) Public Dashboard. https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/fda-adverse-event-monitoring-system-aems-public-dashboard

7. Janiczak S, Tanveer S, Tom K, Zhang R, Ma Y, Wolf L, Muñoz MA. (2025). An Evaluation of Duplicate Adverse Event Reports Characteristics in the Food and Drug Administration Adverse Event Reporting System. *Drug Safety*. https://link.springer.com/article/10.1007/s40264-025-01560-7

8. Response to Xing et al.: post-marketing safety concerns with Lecanemab: a pharmacovigilance study based on the FDA adverse event reporting system database. *Alzheimer's Research & Therapy*. https://link.springer.com/article/10.1186/s13195-025-01735-5

9. Utility and limitations of the FDA adverse events reporting system public dashboard for safety analyses: a case study with vesicular monoamine transporter 2 inhibitors. https://www.tandfonline.com/doi/full/10.1080/14740338.2025.2588634

10. Smith RV, Havens JR, Walsh SL. (2016). Gabapentin misuse, abuse and diversion: a systematic review. *Addiction*, 111(7), 1160-1174. https://onlinelibrary.wiley.com/doi/abs/10.1111/add.13324 (DOI: 10.1111/add.13324)

11. Peckham AM, Ananickal MJ, Sclar DA. (2018). Gabapentin use, abuse, and the US opioid epidemic: the case for reclassification as a controlled substance and the need for pharmacovigilance. *Risk Management and Healthcare Policy*, 11, 109-116. https://www.dovepress.com/gabapentin-use-abuse-and-the-us-opioid-epidemic-the-case-for-reclassif-peer-reviewed-fulltext-article-RMHP (DOI: 10.2147/RMHP.S168504)

12. Fugelstad A, Ågren G, Ramstedt M, Thiblin I, Hjelmström P. Oxycodone-related deaths in Sweden 2006-2018. https://www.sciencedirect.com/science/article/pii/S0376871622001399

---

## Verification notes

- Source 3's original citation (in an earlier draft of this file) pointed to a fabricated URL that did not correspond to this paper. Corrected after a full re-verification pass in which every reference was individually checked against its actual source content.
- Source 5 is a preprint and has not undergone peer review. It is cited here only to support that polypharmacy-driven presentation is an observed pattern in this specific FAERS case series, not as an established, peer-reviewed finding.
- Source 1 may reflect a March 2026 FDA platform rename (FAERS to AEMS); content is unchanged, only the branding and possibly the URL.

## Notes / decisions not tied to a single external source

- **Deduplication:** a report can mention multiple target drugs and therefore appear in multiple per-drug API searches; handled via a `seen_report_ids` set during database construction (`build_database.py`) so each unique `safetyreportid` is only inserted once. This is distinct from FAERS's own internal duplicate-report problem [7], which concerns the same real-world event being submitted to FDA more than once by different reporters; our deduplication does not and cannot detect or fix that underlying issue, only the "same report returned by multiple drug searches" issue.
- **Drug name matching bug:** exact string matching against target drug names missed real variants (suffixes, formatting, combination drug names), silently dropping approximately 35% of relevant reports. Fixed by switching to substring matching plus a cleanup function mapping messy variants to their clean target drug name. Brand names (e.g. LANTUS for Insulin glargine, ZOLOFT for Sertraline, LIPITOR for Atorvastatin) are not matched to their generic drug and remain a known limitation.
- **Age unit bug:** patientonsetage mixed six units (Decade, Year, Month, Week, Day, Hour, coded 800-805) without conversion, producing implausible values (max recorded age of 33,071). Fixed with a new engineered feature, patientonsetage_years, converting every value to years based on its recorded unit code.