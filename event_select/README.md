# A Python program to select events using K-means

## files

+ select_event.py: main part of the code
 
    usage:
    ```sh
    python select_event.py data_ziyi 600 300
    ```
    select 600 events, with depth lower than 300km, and use data_ziyi as the catalog file.

    output:

    a file named as [input file name].selected.

+ data_ziyi

    my region catalog.

+ gmt.sh

    use gmt to plot the region map.

## package required

+ pandas
+ sklearn
+ numpy