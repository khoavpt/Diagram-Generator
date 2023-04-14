<<<<<<< HEAD
# Diagram generator
The Diagram Generator is a tool to help you create diagrams for your geometry Olympiad problems. Simply type in the description of your problems and wait for the result. It can be used to create simple geometric figures, like points and lines, or more complicated figures, like circles and polygons, with lots of different customizations.

## Requirements
- numpy==3.6.2
- Flask==2.2.2
- tqdm==4.46.0
- matplotlib==3.2.1
- tensorflow>=2.4.0

## How it works
How it works?
The process can be divided into two parts: Extract information and generate diagrams.
- Information from the user’s inputs is extracted using a technique called rule-based matching, which is extracting information in a document using a combination of patterns. In this program, I only use some simple patterns that often appear in Vietnamese geometry Olympiad problems, which answers why the program still struggles a lot in trying to understand long and complex sentences.
- And finally, the diagram generation part was done using GMB(Geometry Model Builder). The extracted information is converted to GMBL(Geometry Model Builder Language), which is required for GMB to generate diagrams.

## Introduction video:
https://www.youtube.com/watch?v=KyRtHmdgo3E&t=1s

## Note:
Every files in the GMB folder is from https://github.com/rkruegs123/geo-model-builder 


=======
# Diagram generator
The Diagram Generator is a tool to help you create diagrams for your geometry Olympiad problems. Simply type in the description of your problems and wait for the result. It can be used to create simple geometric figures, like points and lines, or more complicated figures, like circles and polygons, with lots of different customizations.

## Requirements
- numpy==3.6.2
- Flask==2.2.2
- tqdm==4.46.0
- matplotlib==3.2.1
- tensorflow>=2.4.0

## How it works
How it works?
The process can be divided into two parts: Extract information and generate diagrams.
- Information from the user’s inputs is extracted using a technique called rule-based matching, which is extracting information in a document using a combination of patterns. In this program, I only use some simple patterns that often appear in Vietnamese geometry Olympiad problems, which answers why the program still struggles a lot in trying to understand long and complex sentences.
- And finally, the diagram generation part was done using GMB(Geometry Model Builder). The extracted information is converted to GMBL(Geometry Model Builder Language), which is required for GMB to generate diagrams.

## Introduction video:
https://www.youtube.com/watch?v=KyRtHmdgo3E&t=1s

## Note:
Every files in the GMB folder is from https://github.com/rkruegs123/geo-model-builder 


>>>>>>> 30b426fd7273bf2b765c931b40ac3fbf316e2e5b
