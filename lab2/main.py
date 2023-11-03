import pandas as pd

from ipcs import Mmap, SharedMemoryIpc, File, Queue
from testing_process import TestingProcess


def main():
    tester = TestingProcess()
    ipcs_tests = pd.DataFrame(columns=tester.PARAMS)
    for ipc in [Mmap(), SharedMemoryIpc(), File(), Queue()]:
        ipc.create_test_data()
        ipc_results = tester.test(ipc)
        ipcs_tests = pd.concat([ipcs_tests, pd.DataFrame(ipc_results)], ignore_index=True)
        ipc.delete_test_data()
    print('Final results')
    for param in tester.PARAMS:
        max_row = ipcs_tests.loc[ipcs_tests[param].idxmax()]
        min_row = ipcs_tests.loc[ipcs_tests[param].idxmin()]
        print(f'\t{param.capitalize()}')
        print(f'\t\tMax: {max_row[param]:.10f} with ipc: {max_row["ipc"]}')
        print(f'\t\tMin: {min_row[param]:.10f} with ipc: {min_row["ipc"]}')
    ipcs_tests.to_excel('ipcs.xlsx', index=False)


if __name__ == "__main__":
    main()
