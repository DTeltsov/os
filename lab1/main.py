from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from blocking import BlockingTcp, BlockingUdp
from non_blocking import NonBlockingTcp, NonBlockingUdp
from test_socket import SocketTest


def main():
    sockets = [BlockingTcp(), NonBlockingTcp(), BlockingUdp(), NonBlockingUdp()]
    port = 1
    results = {}
    with ThreadPoolExecutor(max_workers=1) as executor:
        for sock in sockets:
            sock.port = int(f'5432{port}')
            executor.submit(sock.test)
            port += 1
    for param in SocketTest.get_df_headers():
        results[param] = {str(sock): sock.test_results.get(param) for sock in sockets}
    df = pd.DataFrame.from_dict(
        {(i, j): results[i][j] for i in results.keys() for j in results[i].keys()}, orient='index'
    )
    df.to_excel('socket_results.xlsx')


if __name__ == '__main__':
    main()
