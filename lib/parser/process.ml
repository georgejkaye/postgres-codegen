let parse_file_contents s =
  Angstrom.parse_string Statement.statements ~consume:All s
