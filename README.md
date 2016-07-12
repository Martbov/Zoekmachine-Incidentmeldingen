# Zoekmachine Incidentmeldingen
De repository voor de zoekmachine om incidentmeldingen te doorzoeken

De zoekmachine is geschreven in Python 3.5 met behulp van PyQt4. Het daarom van belang dat beiden geïnstalleerd zijn op het systeem.
Anaconda (https://www.continuum.io/downloads) biedt een volledige installatie van de meest recente Python versie in combinatie met andere packages, waaronder PyQt4. Afhankelijk van uw systeem dient u de juiste versie te installeren, maar kies in ieder geval Python 3.5 of hoger. De zoekmachine is platform onafhankelijk, maar let wel goed op welke installatie u kiest. Voor Windows dient er gekozen te worden voor de x64 of de x32 installatie. Daarnaast is het van belang dat u Anaconda installeert op een locatie die u later makkelijk terug kunt vinden.

Nadat u Anaconda geïnstalleerd heeft, kunt u deze repository downloaden. Op het moment van schrijven kan dit met de groene 'Clone or download' button rechtsboven op het scherm. U dient vervolgens op 'Download ZIP' te klikken zodat dit bestand gedownload wordt. Als u dit bestand uitgepakt heeft, ziet u vijf bestanden:
- icon.png:   Het pictogram voor de applicatie.
- README.md:  Het README bestand met de installatie- en gebruikshandleiding.
- Screenshot zoekmachine.png: Een screenshot van de zoekmachine om voor gebruik te zien hoe deze er uit ziet.
- searchTool.py: De broncode van de zoekmachine. Pas dit bestand niet aan.
- searchToolWindows.pyw: De broncode en tevens het programma voor Windows. Pas dit bestand niet aan.

Indien u Windows gebruikt, kunt u het programma gebruiken door dubbel te klikken op het searchToolWindows.pyw bestand. Als dit de eerste keer is dat u het programma gebruikt, moet u een programma kiezen om het .pyw bestand te openen. Blader hiervoor naar de locatie waar u Ananconda geïnstalleerd heeft en kies voor het pythonw bestand.
Als het programma opstart, wordt u gevraagd om te bladeren naar het excelbestand met incidentmeldingen. Kies het bestand dat u wilt gebruiken en klik op 'Open'.
De zoekmachine heeft nu het bestand geopend en u kunt met behulp van de drie bovenstaande velden zoektermen invoeren. Voor de velden twee en drie kunt een Boolean zoekwaarde ingeven om uw zoekopdracht nauwkeuriger te maken.
