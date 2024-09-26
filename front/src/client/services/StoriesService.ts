/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StoriesListResponse } from '../models/StoriesListResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StoriesService {
    /**
     * Get List All Stories
     * @returns StoriesListResponse Successful Response
     * @throws ApiError
     */
    public static getListAllStories(): CancelablePromise<StoriesListResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stories',
        });
    }
}
