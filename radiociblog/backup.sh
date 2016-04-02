echo "## BACKUP del db remoto ##"
echo "\tloggarsi con l'utente e la password di GAE se lo chiede"

temp="/tmp/"
daten=`date +%y%m%d%H%M%S`
outn=$temp$daten".json"
backup_path=./Backup
filename=$backup_path"/BACKUP-"$daten".tar.bz2"
python manage.py remote dumpdata --all --verbosity 0 > $outn
echo " - compressione e pulizia"
tar -cSjvf $filename $outn
md5sum $filename > $filename".md5"
rm $outn
echo " - backup "$filename" effettuato"
