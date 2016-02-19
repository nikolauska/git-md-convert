# Requirements Analysis

## Intro
This document contains use cases, technical requirements.

## Actors
- Developer - Produces markdown documentation to repository with   
- Manager/organization - Requires markdown documentation in pdf format where it can easily be printed

## User stories
- Developer wants to produce document in markdown which different version control sites support
- Manager/Organization wants documentation that can be saved in printed format or simple to use pdf format
- Developer wants to host documentation on separate place as just plain html

## Use cases

#### Host html on separate server

**Actor**  
Developer

**Description**  
Developer wants to host his/her markdown documentation as plain html on separate hosting platform

**Precondition**  
Must have markdown documentation

**Usual event order**
1. Use convert python script with wanted repository
2. Copy html files from html folder to wanted location

**Exceptions**
- Unable to connect to internet
    - If old data is still saved, that will be used
    - Should wait for connection to return

#### Convert to pdf for printing

**Actor**  
Manager/Organization

**Description**  
Manager/Organization wants documentation written in markdown to pdf to easily print it.

**Precondition**  
Must have markdown documentation

**Usual event order**
1. Use convert python script with wanted repository
2. Print pdf files on pdf folder

**Exceptions**
- Unable to connect to internet
    - If old data is still saved, that will be used
    - Should wait for connection to return
