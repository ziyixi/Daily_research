J="A120/35/50/6i"
R="20/180/-25/90"
PS="region.ps"
PDF="region.pdf"

gmt psbasemap -J$J -R$R -Ba -BWSen -P -K > $PS
gmt pscoast -J -R  -S167/194/223 -K -O >> $PS

awk '{print $4,$3}' data_ziyi |gmt psxy -J -R -St0.07c -Gblack -K -O >> $PS
awk '{print $4,$3}' data_ziyi.selected |gmt psxy -J -R -St0.07c  -Gred -K -O >> $PS

ps2pdf $PS $PDF
