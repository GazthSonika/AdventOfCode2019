
#include <iostream>
#include <fstream>
#include <vector>
#include <sys/time.h>

using namespace std;

/**
 * Gets all file ane parse "\n" separated integers
 */
vector<int> getData(const string& filename){
    vector<int> masses = {};
    int a;
    fstream data(filename);    
    while(data >> a){
        masses.push_back(a);
    }
    return masses;
}

inline int getFuelAmountA(int mass){
    return mass / 3 - 2;
}

int getFuelAmountB(int mass){
    int fuel = 0;
    int tmp_fuel = getFuelAmountA(mass);
    while(tmp_fuel > 0){ // do while would look beter but less clear
        fuel += tmp_fuel;
        tmp_fuel = getFuelAmountA(tmp_fuel);
    }
    return fuel;
}

void solve(){
    vector<int> masses = getData("day1_a.txt");
    int answerA = 0;
    int answerB = 0;
    for(int &mass: masses){        
        answerA += getFuelAmountA(mass);
        answerB += getFuelAmountB(mass);
    }
    
    cout << "Answer A: " << answerA << endl;
    cout << "Answer B: " << answerB << endl;
}

// void solveAndBench(int tries=1){
//     // Load data  then benchchmark it
//     vector<int> masses = getData("day1_a.txt");
//     int answerA = 0;
//     int answerB = 0;

//     struct timeval tp;
//     gettimeofday(&tp, NULL);
//     long int start = tp.tv_sec * 1000 + tp.tv_usec / 1000;
//     for(int i=0; i<tries; i++){
//         answerA = 0;
//         answerB = 0;
//         for(int &mass: masses){        
//             answerA += getFuelAmountA(mass);
//             answerB += getFuelAmountB(mass);
//         }
//     }    
//     gettimeofday(&tp, NULL);
//     long int end = tp.tv_sec * 1000 + tp.tv_usec / 1000;

//     cout << "Execution time: " << end-start << "ms for " << tries << " tries" << endl;
//     cout << "Answer A: " << answerA << endl;
//     cout << "Answer B: " << answerB << endl;
// }

int main(){               
    /*
     * dont know fancy stuff with lambdas and dont remember function reference ;( 
     * 
     * g++ -O3 day1.cpp -o main && ./main
     */    
    solve();
    // solveAndBench(1000000);
    return 0;
}
