#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

void server()
{
    WSADATA wsaData;
    SOCKET serverSocket, clientSocket;
    struct sockaddr_in serverAddress, clientAddress;
    int clientAddressLength;
    char buffer[1024];
    char response[1024];
    int variable = 0;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        printf("Failed to initialize Winsock.\n");
        return;
    }

    // Create server socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET)
    {
        printf("Failed to create server socket.\n");
        WSACleanup();
        return;
    }

    // Set server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddress.sin_port = htons(12345);

    // Bind server socket to the specified address and port
    if (bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == SOCKET_ERROR)
    {
        printf("Failed to bind server socket.\n");
        closesocket(serverSocket);
        WSACleanup();
        return;
    }

    // Listen for incoming connections
    if (listen(serverSocket, 1) == SOCKET_ERROR)
    {
        printf("Failed to listen for incoming connections.\n");
        closesocket(serverSocket);
        WSACleanup();
        return;
    }

    printf("Server is listening on localhost:12345\n");

    // Accept a client connection
    clientAddressLength = sizeof(clientAddress);
    clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddress, &clientAddressLength);
    if (clientSocket == INVALID_SOCKET)
    {
        printf("Failed to accept client connection.\n");
        closesocket(serverSocket);
        WSACleanup();
        return;
    }

    printf("Connected to: %s:%d\n", inet_ntoa(clientAddress.sin_addr), ntohs(clientAddress.sin_port));

    // Main server loop
    while (1)
    {
        char client[8];
        //sprintf(client, "client%d", (rand() % 2) + 1);

        if (variable < 100)
        {
            sprintf(response, "%s:%d", "client1", variable);
            send(clientSocket, response, strlen(response), 0);
            printf("Sent to client: %s\n", response);
        }

        int bytesRead = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesRead <= 0)
            break;

        buffer[bytesRead] = '\0';

        char* token = strtok(buffer, ":");
        char rec_client[8];
        strcpy(rec_client, token);

        token = strtok(NULL, ":");
        int rec_value = atoi(token);

        variable = rec_value;
        printf("Received from client: %s\n", buffer);
    }

    // Close the client and server sockets
    closesocket(clientSocket);
    closesocket(serverSocket);

    // Cleanup Winsock
    WSACleanup();
}

int main()
{
    server();
    return 0;
}