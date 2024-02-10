#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

void client2()
{
    const char* relayHost = "localhost";
    const int relayPort = 54321;

    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        fprintf(stderr, "Failed to initialize Winsock.\n");
        return;
    }

    SOCKET relaySocket = socket(AF_INET, SOCK_STREAM, 0);
    if (relaySocket == INVALID_SOCKET)
    {
        fprintf(stderr, "Failed to create relay socket.\n");
        WSACleanup();
        return;
    }

    // Prepare the address structure
    struct sockaddr_in relayAddress;
    relayAddress.sin_family = AF_INET;
    relayAddress.sin_port = htons(relayPort);
    relayAddress.sin_addr.s_addr = inet_addr(relayHost);

    // Connect to the relay server
    if (connect(relaySocket, (struct sockaddr*)&relayAddress, sizeof(relayAddress)) < 0)
    {
        fprintf(stderr, "Failed to connect to the relay server.\n");
        closesocket(relaySocket);
        WSACleanup();
        return;
    }

    while (1)
    {
        char data[1024];

        printf("test0\n");

        int bytesReceived = recv(relaySocket, data, sizeof(data), 0);

        printf("test1\n");

        if (bytesReceived > 0)
        {
            data[bytesReceived] = '\0';

            printf("test2\n");

            char client[32];
            int value;
            sscanf(data, "%[^:]:%d", client, &value);

            printf("test3\n");

            value++;

            snprintf(data, sizeof(data), "%s:%d", "client2", value);
            send(relaySocket, data, strlen(data), 0);

            printf("test4\n");
        }
    }

    // Close the socket and cleanup
    closesocket(relaySocket);
    WSACleanup();
}

int main()
{
    client2();
    return 0;
}