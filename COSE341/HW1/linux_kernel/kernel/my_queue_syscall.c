#include <linux/syscalls.h>
#include <linux/kernel.h>
#include <linux/linkage.h>
#include <linux/slab.h>

#define MAX_QUEUE 500

int queue[MAX_QUEUE]; // queue로 사용할 정수 배열
int front = 0; // queue의 front index
int rear = 0; // queue의 rear index

// enqueue를 수행하는 시스템 콜 함수, 정수 변수 하나를 인자로 가짐
SYSCALL_DEFINE1(oslab_enqueue, int, data) {
    int i = 0; // 반복문에서 사용할 변수

    if (rear >= MAX_QUEUE) {
        printk(KERN_INFO "[Error] - QUEUE IS FULL--------------------\n");
        return -2;
    } // queue가 꽉 찼으면 큐가 꽉 찼다고 에러를 출력하고 -2를 반환

    for (i = front; i < rear; i++) {
        if (queue[i] == data) {
            printk(KERN_INFO "[Error] - Already existing value\n");
            return data;
        }
    } // queue의 처음부터 마지막까지 지나가면서 enqueue하려는 값과 중복되는 값이 없는지 확인

    printk(KERN_INFO "[System call] oslab_enqueue(); -----\n");

    queue[rear++] = data; // queue의 rear에 새로운 값을 추가하고 rear index를 +1

    printk(KERN_INFO "Queue Front--------------------\n");

    for (i = front; i < rear; i++)
        printk(KERN_INFO "%d\n", queue[i]);

    printk(KERN_INFO "Queue Rear--------------------\n");

    return data;
}

// dequeue를 수행하는 시스템 콜 함수
SYSCALL_DEFINE0(oslab_dequeue) {
    int i = 0; // 반복문에서 사용할 변수
    int result = 0; // dequeue 된 값

    if (front == rear) { // 큐가 비어있다면 비었다고 출력 후 함수 종료
        printk(KERN_INFO "[Error] - EMPTY QUEUE--------------------\n");
        return -2;
    }

    printk(KERN_INFO "[System call] oslab_dequeue(); -----\n");

    result = queue[front++]; // queue의 front에서 값을 dequeue한 후 front index +1

    for (i = front; i < rear; i++) {
        queue[i - front] = queue[i]; // dequeue 후 배열 앞 부분이 비어서 사용 못하는 것을 막기 위해 값을 한 칸씩 옮겨 줌
    }

    rear -= front;
    front = 0;

    printk(KERN_INFO "Queue Front--------------------\n");

    for (i = front; i < rear; i++)
        printk(KERN_INFO "%d\n", queue[i]);

    printk(KERN_INFO "Queue Rear--------------------\n");

    return result;
}
