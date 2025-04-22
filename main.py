from tbs_etl.parsing.parse_990pf import parse_990pf_file


if __name__ == "__main__":
    # TEMPORARILY IGNORE CLI ARGS AND RUN TEST FIXTURES:
    parsed = parse_990pf_file("test_file/ford_2013.xml")
    # parsed = parse_990pf_file("test_file/foundation_to_promote_open_society_2021.xml")
    for grant in parsed:
        print(grant)
    # import sys
    # if len(sys.argv) < 2:
    #     print("Usage: python main.py <path_to_990pf_xml>")
    # else:
    #     # parsed = parse_990pf_file(sys.argv[1])
    #     parsed = parse_990pf_file("test_file/ford_2013.xml")
    #     parsed = parse_990pf_file("test_file/foundation_to_promote_open_society_2021.xml")
    #     for grant in parsed:
    #         print(grant)


