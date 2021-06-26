#include <stdio.h>

int count_node(int h) 
{
    int sum = h;
    for(int i=1; i<=h-2; i++) sum += count_node(i);
    return sum;
}

int count_minimum_node(int h) { return count_node(h+1); }
int main(){
	printf("%d", count_minimum_node(6));
}
