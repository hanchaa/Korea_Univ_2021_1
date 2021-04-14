#include <linux/syscalls.h>
#include <linux/kernel.h>
#include <linux/linkage.h>
#include <linux/slab.h>

typedef struct queue_node {
    int data;
    struct queue_node *next;
} Node; // ť�� ���� ���Ǵ� ����ü

typedef struct queue {
    Node *front; // ť�� ù��° ��带 ����Ű�� ������
    Node *rear; // ť�� ������ ��带 ����Ű�� ������
    int size; // ť�� ���� ����ִ� ����� ������ ��Ÿ���� ����
} Queue; // ť�� ������ ������ �ִ� ����ü

Queue q;

SYSCALL_DEFINE1(oslab_enqueue, int, a) {
    Node *i = q.front; // loop���� ����� ����

    if (temp == NULL) {
        printk(KERN_INFO "[Error] - QUEUE IS FULL--------------------\n");
        return -2;
    } // �޸𸮰� �������� �ʴٸ� ť�� �� á�ٰ� ����ϸ� �Լ� ����

    while (i != NULL) {
        if (i->data == a) {
            printk(KERN_INFO "[Error] - Duplicate integer in queue--------------------\n");
            return -2;
        }
        i = i->next;
    } // ť�� ù ��° ������ ������ ������ �������鼭 �ߺ��� �����Ͱ� �ִ��� Ȯ��

    printk(KERN_INFO "[System call] oslab_enqueue(); -----\n");

    Node *temp = (Node *)kmalloc(sizeof(Node), GFP_KERNEL); // malloc�� ���ؼ� ���� �߰��� �����͸� ���� ��带 ����
    temp->data = a;
    temp->next = NULL;

    if (q.size == 0) { // ť�� ����ִٸ� ����Ʈ�� ���� ��带 ��� �� ���� �Ҵ�
        q.front = q.rear = temp;
    }
    else { // ť�� ������ ����� ���� ���� �� ��� �Ҵ� / ť�� ���� ��带 �� ���� ����
        (q.rear)->next = temp;
        q.rear = temp;
    }

    q.size += 1;

    printk(KERN_INFO "Queue Front--------------------\n");

    i = q.front;

    while (i != NULL) {
        printk(KERN_INFO "%d\n", i->data);
        i = i->next;
    }

    printk(KERN_INFO "Queue Rear--------------------\n");

    return a;
}

SYSCALL_DEFINE0(oslab_dequeue) {
    Node *i = NULL; // loop�� ���� ����
    Node *temp = NULL; // pop �Ǵ� ��带 �ӽ÷� ������ ����
    int res = 0; // pop �Ǵ� ���� ������ ����

    if (q.size == 0) { // ť�� ����ִٸ� ����ٰ� ��� �� �Լ� ����
        printk(KERN_INFO "[Error] - EMPTY QUEUE--------------------\n");
        return -2;
    }

    printk(KERN_INFO "[System call] oslab_dequeue(); -----\n");

    temp = q.front;
    res = temp->data;
    q.front = temp->next;
    q.size -= 1;
    kfree(temp);
    // ť�� ����Ʈ ��带 pop �� res�� pop �� ����� data�� �ű�� ť�� ����Ʈ ���� pop �� ����� ���� ���� ����, ť�� ����ִ� ��� ���� ����, pop �� ���� �޸� �Ҵ� ����

    printk(KERN_INFO "Queue Front--------------------\n");

    i = q.front;
    while (i != NULL) {
        printk(KERN_INFO "%d\n", i->data);
        i = i->next;
    }

    printk(KERN_INFO "Queue Rear--------------------\n");

    return res;
}
