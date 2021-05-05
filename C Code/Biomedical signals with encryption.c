// -------------------------------- //
// 讀取raw檔裡的生理訊號，輸出txt檔   //
// 用混沌系統做加密解密               //
// -------------------------------- //

#include <iostream>

#define height  12500
#define	width	8
 
typedef short BYTE;	 //define BYTE

double x1,x2,x3,x1s,x2s,x3s;
double _y1,y2,y3,y1s,y2s,y3s;
double e1,e2;
double Kp,u1,u2;
int i,j,k;
int num_a,num_n,num,num_data,sum,total,total_row;
 
int main()
{   
//----------------------Initial-----------------------    
    x1=0.001;x2=-0.012;x3=0.015;  // initial conditions
    _y1=0.0011;y2=-0.0126;y3=0.0157;  // initial conditions
    Kp=0.25; 
    k=0;
    num_a = 0,num_n = 0,num = 0,num_data = 0,sum = 0,total = 0,total_row = 12500;

    FILE *fp = NULL;
    
    float Data2[height][width];  
    BYTE Data1[height][width];
    BYTE CHECK[width];
    BYTE *ptr;
    
    char path[256] = "D:\\test01.raw";   //read the data
    int data[11] = {10, 2, 1, 21, 2, 2, 16, 256, 2, 200, 8};    // data formation
    char data_ascii[503];   //10+21+16+256+200
    int data_number[9];     //2+1+2+2+2
    int flag[] = {0, 0, 0, 0, 0};

//------------------Open the raw file------------------
    if((fp = fopen( path, "rb" )) == NULL)
    {
        printf("Can not open the raw file\n");
        return 0;
    }
    else
    {
        printf("Read OK\n\n");
    } 
    
//---------------Turn the data into array---------------   	
    ptr = (BYTE*)malloc( width * height * sizeof(BYTE) );

// ---------------Definition of raw data ---------------
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
        ptr ++;
        num ++;
        if (num == data[k]){
            k ++;
            num = 0;
        }
    }

// -------------------Save the data-------------------
    for( i = 0; i <= total_row; i++ )
    {
        for( j = 0; j < width ; j ++ )
        {            
            fread( ptr, 1, 1, fp );
            total ++;
            CHECK[j] = *ptr;
            Data1[i][j] = *ptr;
            printf("Data = %d ",Data1[i][j]);

// --------------------Eecryption--------------------  
            e1 = x2*x2 + 0.1*x3;
            u1 = x2*x2 + 0.1*x3 + Kp*e1;   //u1 = x2*x2 - Kp*(-e1);
            
            x1s = 1.76 - (x2*x2) - 0.1*x3;
            x2s = x1; x3s = x2;
            x1 = x1s; x2 = x2s; x3 = x3s;

            Data2[i][j] = *ptr / x1;
            
// --------------------Decryption-------------------- 
            e2 = y2*y2 + 0.1*y3 ;
            u2 = (y2*y2 + 0.1*y3 - u1) + Kp*e2 ;   //u[i] = Kp*P[i]
            
            y1s = 1.76 - (y2*y2) - 0.1*y3 + u2;
            y2s = _y1; y3s = y2;
            _y1 = y1s; y2 = y2s; y3 = y3s;

            Data1[i][j] = int(Data2[i][j] * _y1 + 0.5);  //rounding

            printf("Eecryption : %f\tDecryption : %d  \n",Data2[i][j],Data1[i][j]);
            // printf("x1 = %.6f\ty1 = %.6f\te2 = %.6f\n",x1,_y1,e2-e1);

// ---------------Check if it is the end--------------- 
            if (j == 7){
                for (k = 0; k < width ; k++){
                    sum = sum + CHECK[k];
                }
                    
                if (sum == 0){
                    total_row = total / 8 - 2;
                }
            sum = 0;
            }
            ptr++;
        }
        for (k = 0; k < width ; k++){
            CHECK[k] = 0;
        }
    }
    fclose(fp);
}
