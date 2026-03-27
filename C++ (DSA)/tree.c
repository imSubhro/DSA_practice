#include<stdio.h>
#include<stdlib.h>

struct node{
    int data;
    struct node* left;
    struct node* right;

};


struct node* newNode(int data){
    
    struct node*node= (struct node*)malloc(sizeof(struct node));

    node->data = data;
    node->left= NULL;
    node->right= NULL;

    return (node);
}

void inorder(struct node* node)
{
    if(node==NULL)
    return;

    inorder(node->left);

    printf("%d ", node->data);

    inorder(node->right);
}


void preorder(struct node* node){

    if(node ==NULL)
    return;

    printf("%d ", node->data);
    preorder(node->left);
    preorder(node->right);

}


void postorder(struct node* node){

    if(node ==NULL)
    return;

    postorder(node->left);
    postorder(node->right);
    printf("%d ", node->data);

}


int main(){
    struct node* root = newNode(1);

    root->left =newNode(2);
    root->right = newNode(3);
    root->left->left= newNode(4);
    root->left->right =newNode(5);

    printf("Inorder traversal of binary tree is: ");
    inorder(root);

    // printf("preorder traversal of binary tree is: ");
    // preorder(root);

    // printf("postorder traversal of binary tree is: ");
    // postorder(root);


    return 0;
}
