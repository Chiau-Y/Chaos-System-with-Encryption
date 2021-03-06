// -------------------------------- //
// 讀取raw檔裡的生理訊號，輸出txt檔 //
// -------------------------------- //

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
#define	height	256
#define	width	256
 
typedef unsigned char  BYTE;	 //define BYTE
 
int main()
{
	FILE *fp = NULL;
	
	BYTE B[height][width];
	BYTE *ptr;
	
	char path[256] = "D:\\test01.raw";   //read the data
	char outpath[256] = "D:\\Master\\123.txt";  //save the data
   	int data[11] = {10, 2, 1, 21, 2, 2, 16, 256, 2, 200, 8};    // data formation
	char data_ascii[503];   //10+21+16+256+200
   	int data_number[9];     //2+1+2+2+2

	int i,j,num_a = 0,num_n = 0,num = 0,k = 0,num_data = 0;
	
	 //open the raw file
	if((fp = fopen( path, "rb" )) == NULL)
	{
	    printf("Can not open the raw filen\n");
	    return 0;
	}
	else
	{
	printf("Read OK\n\n");
	} 
	
	 // turn the data into array   	
	ptr = (BYTE*)malloc( width * height * sizeof(BYTE) );
	
	// the first 512 data we do not use it 
	for(i = 0; i < 512; i++){
		fread( ptr, 1, 1, fp );
		if (k == 0 || k == 3 || k == 6 || k == 7 || k == 9 )
		{
		    data_ascii[num_a] = *ptr;
		    num_a ++;
		}
		else {
		    data_number[num_n] = *ptr; 
		    num_n ++;
		}   
		ptr++;
			num ++;
			if (num == data[k]){
				k ++;
				num = 0;
		}
	}
    
   	// save the biomedical signals
	for( i = 0; i < height; i++ )
	{
		for( j = 0; j < width ; j ++ )
		{
			fread( ptr, 1, 1, fp );
			B[i][j]= *ptr;	 //array
			ptr++;
		}

	}
	fclose(fp);
	
    	num_a = 0; num_n = 0;k = 0;num = 0;
	if( ( fp = fopen( outpath,"wb" ) ) == NULL )
	{
	    printf("can not create the raw_image : %s\n", outpath );
	    return 0;
	}
    
	for(i = 0; i < 512; i++){
		if (k == 0 || k == 3 || k == 6 || k == 7 || k == 9 )
		{
			fprintf(fp, "%c", data_ascii[num_a]);  
			num_a ++;
		}
		else {
			fprintf(fp, "%d", data_number[num_n]);  
			num_n ++;
		}   
		num ++;
		if (num == data[k]){
			num = 0;
			k ++;
			fprintf(fp, "\n");
		}
	}

    num = 0;
	fprintf(fp, "%-5d ", num_data);
	for( i = 0; i < height; i++ )
	{
	    for( j = 0; j < width ; j ++ )
		{
			fprintf(fp, "%3d ", B[i][j]);
			num++;
			if (num == data[10]){
				num_data ++;
				fprintf(fp, "\n");
				fprintf(fp, "%-5d ", num_data);
				num = 0;
            		}
		}
	}
	
	fclose(fp);
}
