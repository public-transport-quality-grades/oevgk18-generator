with import <nixpkgs> {}; let
  records = with python36.pkgs;
    buildPythonPackage {
      name = "records-0.5.2";
      doCheck = false;
      propagatedBuildInputs = [
        sqlalchemy
        tablib
        docopt
        unicodecsv
        psycopg2
      ];
      src = fetchurl {
        url = "https://pypi.python.org/packages/89/f8/aec41f062568eb8a027f26fe1d2aaa30441e6bbe65896f7ad70dd5cc895e/records-0.5.2.tar.gz";
        sha256 = "11inmhiggw3skab9g1cp9bdpi7kx0ayrbcdvjd275fzgx0svm313";
      };
    };

  geojson = with python36.pkgs;
    buildPythonPackage {
      name = "geojson-2.3.0";
      doCheck = false;
      src = fetchurl {
        url = "https://pypi.python.org/packages/ee/5b/8785c562d2bc910a5effada38d86925afa3d1126ddb3d0770c8a84be8baa/geojson-2.3.0.tar.gz";
        sha256 = "06ihcb8839zzgk5jcv18kc6nqld4hhj3nk4f3drzcr8n8893v1y8";
      };
    };
in
(python3.withPackages (
  pkgs: with pkgs;
  [
    records
    shapely
    geojson

    # dev requirements
    pytest
    pytest-sugar
    pytestcov
  ]
)).env
  