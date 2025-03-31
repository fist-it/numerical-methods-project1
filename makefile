run:
	python3 main.py


show:
	@kitten icat ./figures/*.png # Show the image

clean:
	@rm -f ./figures/*.png # Remove images

sprawko: konwertuj
	sioyek ./sprawozdanie/sprawozdanie.pdf

latex-compile:
	pdflatex -output-directory="./sprawozdanie" ./sprawozdanie.tex

konwertuj:
	pandoc -s ./sprawozdanie.md -o ./sprawozdanie/sprawozdanie.pdf
