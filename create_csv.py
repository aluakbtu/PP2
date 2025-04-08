import csv

filename = 'data/phone_book.csv'

with open(filename, 'w', newline='', encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['username', 'phone'])
    writer.writerow(['Alua', 870712345])
    writer.writerow(['Shynar', 874701010])
    writer.writerow(['Bota', 870100035])
    writer.writerow(['Ayana', 877755555])

print("CSV файл успешно создан.")
