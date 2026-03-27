#include <stdio.h>
#include <stdlib.h>

struct node
{
    int roll;
    char name[20];
    struct node *next;
};

struct node *head = NULL;

void create()
{
    struct node *newnode;
    newnode = (struct node*)malloc(sizeof(struct node));
    printf("Enter the roll number: ");
    scanf("%d", &newnode->roll);
    printf("Enter the name: ");
    scanf("%s", newnode->name);
    newnode->next = NULL;
    if(head == NULL)
    {
        head = newnode;
    }
    else
    {
        struct node *temp = head;
        while(temp->next != NULL)
        {
            temp = temp->next;
        }
        temp->next = newnode;
    }
}

void insert()
{
    int pos;
    struct node *newnode, *temp;
    newnode = (struct node*)malloc(sizeof(struct node));
    printf("Enter the roll number: ");
    scanf("%d", &newnode->roll);
    printf("Enter the name: ");
    scanf("%s", newnode->name);
    newnode->next = NULL;
    printf("Enter the position where you want to insert the node: ");
    scanf("%d", &pos);
    if(pos == 1)
    {
        newnode->next = head;
        head = newnode;
    }
    else
    {
        temp = head;
        for(int i = 1; i < pos-1; i++)
        {
            temp = temp->next;
        }
        newnode->next = temp->next;
        temp->next = newnode;
    }
}

void delete()
{
    int pos;
    struct node *temp, *prev;
    printf("Enter the position where you want to delete the node: ");
    scanf("%d", &pos);
    if(pos == 1)
    {
        temp = head;
        head = head->next;
        free(temp);
    }
    else
    {
        temp = head;
        for(int i = 1; i < pos-1; i++)
        {
            temp = temp->next;
        }
        prev = temp;
        temp = temp->next;
        prev->next = temp->next;
        free(temp);
    }
}

void display()
{
    struct node *temp;
    temp = head;
    while(temp != NULL)
    {
        printf("%d %s\n", temp->roll, temp->name);
        temp = temp->next;
    }
}

int main()
{
    int ch;
    while(1)
    {
        printf("1. Create\n2. Insert\n3. Delete\n4. Display\n5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &ch);
        switch(ch)
        {
            case 1:
                create();
                break;
            case 2:
                insert();
                break;
            case 3:
                delete();
                break;
            case 4:
                display();
                break;
            case 5:
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }
    return 0;
}