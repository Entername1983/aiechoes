/* Copy to be used to replace generated one, do not delete */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

// Command to use to generate new api
// npx @hey-api/openapi-ts -i http://localhost:5000/openapi.json -o src/client -c @hey-api/client-fetch

import type { ApiRequestOptions } from "./ApiRequestOptions";
const backendUrl = import.meta.env.VITE_BACKEND_URL;

type Resolver<T> = (options: ApiRequestOptions) => Promise<T>;
type Headers = Record<string, string>;

export type OpenAPIConfig = {
  BASE: string;
  VERSION: string;
  WITH_CREDENTIALS: boolean;
  CREDENTIALS: "include" | "omit" | "same-origin";
  TOKEN?: string | Resolver<string> | undefined;
  USERNAME?: string | Resolver<string> | undefined;
  PASSWORD?: string | Resolver<string> | undefined;
  HEADERS?: Headers | Resolver<Headers> | undefined;
  ENCODE_PATH?: ((path: string) => string) | undefined;
};

export const OpenAPI: OpenAPIConfig = {
  BASE: backendUrl,
  VERSION: "0.1.0",
  WITH_CREDENTIALS: false,
  CREDENTIALS: "include",
  TOKEN: undefined,
  USERNAME: undefined,
  PASSWORD: undefined,
  HEADERS: undefined,
  ENCODE_PATH: undefined,
};
