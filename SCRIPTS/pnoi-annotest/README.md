# PNOI Annotest

## Description

Annotest is for validating the Pnoi dataset and its corresponding annotations, reporting any potential errors or inconsistencies. This script aids in ensuring the quality and integrity of the dataset by identifying issues that may require attention.

## Features

- Dataset Validation: The code base verifies the structure and integrity of the dataset files, ensuring that they adhere to the expected format and naming conventions.

- Annotation Verification: The script checks the annotations associated with the dataset to ensure they are correctly aligned with the corresponding data samples.
  - Labels are within the given set of valid labels and matches annotation scheme.
  - Detail verification of the annotation labels, e.g. duration of breath, inhale-exhale pairs, etc.
  - Cross verify the annotations by different annotators.

- Error Reporting: If any errors or inconsistencies are detected, the code base generates a detailed report highlighting the specific issues found, such as missing files, misaligned annotations, or other potential errors.

## Annotation Scheme

![Annotation Scheme](/media/pnoi-annotation_scheme.png)