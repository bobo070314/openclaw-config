$t = New-Object System.Net.Sockets.TcpClient
try {
    $t.Connect('127.0.0.1', 18900)
    $t.Close()
    exit 0
} catch {
    exit 1
}
