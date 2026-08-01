# Meetily licence disposition

## Verified repository state

The repository README displays a **MIT** licence badge and describes the community project as open source. A standalone `LICENSE` file was not found in the current fork during the Wave 1 review.

## Wave 1 decision

The original DAWN files under `dawn-integration/` may proceed through offline testing because they were independently written and do not copy Meetily implementation code.

Meetily source code, assets or packaged binaries must not be redistributed as part of a commercial DAWN product until the exact upstream licence text and required copyright notice have been restored or otherwise verified from the authoritative upstream source.

## Required before distribution or customer deployment

Record:

1. the authoritative upstream repository and reviewed commit;
2. the complete MIT licence text and copyright notice;
3. any separate licence or commercial restrictions affecting Meetily PRO features;
4. third-party model, transcription, audio and export licences;
5. confirmation that only Community Edition functionality is being adopted unless separate rights are obtained;
6. retained attribution in any redistributed source or package.

## Merge gate

The DAWN contract, schemas, fixtures and offline acceptance tests may become technically merge-ready when CI and the Mac pull-and-test pass. This does not approve redistribution, live recording, microphone access or production deployment.
