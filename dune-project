(lang dune 3.15)

(name postgres_codegen)

(generate_opam_files true)

(source
 (github georgejkaye/postgres-codegen))

(authors "George Kaye")

(maintainers "George Kaye")

(license GPL-v3.0-or-later)

(documentation https://github.com/georgejkaye/postgres-codegen)

(package
 (name postgres_codegen)
 (synopsis "Tool for managing and interacting with postgres sql files")
 (description
  "Tool to manage postgres sql files, running them into the db when updated and generating data access code for interacting with them in other languages")
 (depends
  ocaml
  dune
  core
  core_unix
  re
  angstrom
  fpath
  fmt
  alcotest
  bisect_ppx
  ppx_string
  ppx_deriving
  ppx_compare
  ppx_variants_cov)
 (tags
  (postgres codegen python sql)))
