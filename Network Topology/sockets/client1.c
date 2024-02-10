#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

void client1()
{
    WSADATA wsaData;
    SOCKET clientSocket, relaySocket;
    struct sockaddr_in serverAddress, relayAddress;
    char buffer[1024];
    char response[1024];

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        printf("Failed to initialize Winsock.\n");
        return;
    }

    // Create client socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == INVALID_SOCKET)
    {
        printf("Failed to create client socket.\n");
        WSACleanup();
        return;
    }

    // Set server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = inet_addr("127.0.0.1");
    serverAddress.sin_port = htons(12345);

    // Connect to the server
    if (connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == SOCKET_ERROR)
    {
        printf("Failed to connect to the server.\n");
        closesocket(clientSocket);
        WSACleanup();
        return;
    }

    // Create relay socket
    relaySocket = socket(AF_INET, SOCK_STREAM, 0);
    if (relaySocket == INVALID_SOCKET)
    {
        printf("Failed to create relay socket.\n");
        closesocket(clientSocket);
        WSACleanup();
        return;
    }

    // Set relay address
    relayAddress.sin_family = AF_INET;
    relayAddress.sin_addr.s_addr = htonl(INADDR_ANY);
    relayAddress.sin_port = htons(54321);

    // Bind relay socket to the specified address and port
    if (bind(relaySocket, (struct sockaddr*)&relayAddress, sizeof(relayAddress)) == SOCKET_ERROR)
    {
        printf("Failed to bind relay socket.\n");
        closesocket(clientSocket);
        closesocket(relaySocket);
        WSACleanup();
        return;
    }

    // Listen for incoming connections
    if (listen(relaySocket, 1) == SOCKET_ERROR)
    {
        printf("Failed to listen for incoming connections.\n");
        closesocket(clientSocket);
        closesocket(relaySocket);
        WSACleanup();
        return;
    }

    printf("Client 1 relay node is listening on localhost:54321\n");

    // Accept a relay connection
    SOCKET relayConnSocket;
    struct sockaddr_in relayConnAddress;
    int relayConnAddressLength = sizeof(relayConnAddress);
    relayConnSocket = accept(relaySocket, (struct sockaddr*)&relayConnAddress, &relayConnAddressLength);
printf("cupsaaaaaaaaa");
    if (relayConnSocket == INVALID_SOCKET)
    {
        printf("Failed to accept relay connection.\n");
        closesocket(clientSocket);
        closesocket(relaySocket);
        WSACleanup();
        return;
    }

    

    // Main client loop
    while (1)
    {
        int bytesRead = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesRead <= 0)
            break;

        buffer[bytesRead] = '\0';

        char client[8];
        int value;
        printf("cupsa");
        sscanf(buffer, "%[^:]:%d", client, &value);
        printf("cupsa2");

        if (strcmp(client, "client1") == 0)
        {
            value += 1;
            sprintf(response, "%s:%d", "client1", value);
            send(clientSocket, response, strlen(response), 0);
       
        }

                else if (strcmp(client, "client2") == 0)
        {
            // Send data to relay
            send(relayConnSocket, buffer, strlen(buffer), 0);

            // Receive response from relay
            int bytesReceived = recv(relayConnSocket, response, sizeof(response), 0);
            if (bytesReceived > 0)
            {
                response[bytesReceived] = '\0';
                // Send data back to server
                send(clientSocket, response, strlen(response), 0);
            }
        }
    }

    // Close sockets
    closesocket(clientSocket);
    closesocket(relaySocket);
    closesocket(relayConnSocket);

    // Cleanup Winsock
    WSACleanup();
}

int main()
{
    client1();
    return 0;
}