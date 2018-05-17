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

  rtree = with python36.pkgs;
    buildPythonPackage rec {
      pname = "Rtree";
      version = "0.8.3";

      src = fetchPypi {
        inherit pname version;
        sha256 = "0jc62jbcqqpjcwcly7l9zk25bg72mrxmjykpvfiscgln00qczfbc";
      };

      propagatedBuildInputs = [ libspatialindex ];

      patchPhase = ''
        substituteInPlace rtree/core.py --replace \
          "find_library('spatialindex_c')" "'${libspatialindex}/lib/libspatialindex_c${stdenv.hostPlatform.extensions.sharedLibrary}'"
      '';

      # Tests appear to be broken due to mysterious memory unsafe issues. See #36760
      doCheck = false;
      checkInputs = [ numpy ];

      meta = with stdenv.lib; {
        description = "R-Tree spatial index for Python GIS";
        homepage = https://toblerity.org/rtree/;
        license = licenses.lgpl21;
        maintainers = with maintainers; [ bgamari ];
      };
    };

  generator = with python36.pkgs;
    buildPythonPackage {
      name = "generator";
      doCheck = false;
      src = ./.;
      propagatedBuildInputs = [
        geojson
        shapely
        records
        jsonschema
        ruamel_yaml
        rtree
      ];
    };

in
(python3.withPackages (
  pkgs: with pkgs;
  [
    generator

    # dev requirements
    pytest
    pytest-sugar
    pytestcov
  ]
)).env
  