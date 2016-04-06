red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
reset=`tput sgr0`
debug=false

echo "${green}=================================${reset}"
echo "${green}Goofile Metadata Extractor v. 2.0.${reset}"
echo "${green}This script finds documents for a specified domain, downloads them, then extracts the meta-data.${reset}"
echo "${green}Written by Joe Doran${reset}"
echo "${green}Email: joseph.w.doran@gmail.com, joe.doran@aos5.com${reset}"
echo "${green}=================================${reset}"
echo ""
echo "${yellow}Requires goofile${reset} ==> http://code.google.com/p/goofile"
echo "${yellow}Requires exiftool${reset} ==> http://www.sno.phy.queensu.ca/~phil/exiftool/index.html"
echo ""
if [ $debug == true ];
then
	echo "${yellow}DEBUG mode is on.${reset}"
else
	echo "${yellow}DEBUG mode is off.${reset}"
fi
echo ""
echo -n "${red}Domain: ${reset}"
read domain
echo ""
mkdir $domain
mkdir $domain/web-docs
mkdir $domain/meta-data



echo "${green}[+] ${reset}Gathering .doc"
goofile -d $domain -f doc > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort > $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .docx"
goofile -d $domain -f docx > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .pdf"
goofile -d $domain -f pdf > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .ppt"
goofile -d $domain -f ppt > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .pptx"
goofile -d $domain -f pptx > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .txt"
goofile -d $domain -f txt > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .xls"
goofile -d $domain -f xls > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Gathering .xlsx"
goofile -d $domain -f xlsx > $domain.goofiletmp
grep $domain $domain.goofiletmp | grep -v 'Searching in' | grep -Fv '...' | sort >> $domain/meta-data/$domain.goofileraw
if [ $debug == true ];
then
	cat $domain.goofiletmp
fi



echo "${green}[+] ${reset}Removing tmp files"
rm $domain.goofiletmp



if [ $debug == true ];
then
	cat $domain/meta-data/$domain.goofileraw
fi
echo "${green}[+] ${reset}URLs written to ${green}$domain/meta-data/$domain.goofileraw ${reset}"
echo ""
echo ""
echo ""
echo "${green}{+] ${reset}Downloading all files to ${green}$domain/web-docs/ ${reset}"
wget -i $domain/meta-data/$domain.goofileraw -P $domain/web-docs/
echo "${green}{+} ${reset}Downloads completed to ${green}/$domain/web-docs/ ${reset}"
echo ""
echo ""
echo ""
echo "${green}[+] ${reset}Extracting metadata ${reset}"
find $domain/web-docs/ -maxdepth 1 -type f -exec exiftool {} \+ > $domain/meta-data/$domain.metadatafull
echo "${green}[*] ${reset}Full metadata written to ${green}$domain/meta-data/$domain.metadatafull ${reset}"
cat $domain/meta-data/$domain.metadatafull | grep -v "Tool" | grep -E "(File Name|Company|Author|Creator|Last Modified)" > $domain/meta-data/$domain.metadatausers
echo "${green}[*] ${reset}User metadata written to ${green}$domain/meta-data/$domain.metadatausers ${reset}"

