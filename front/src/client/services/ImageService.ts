/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PreSignedUrlResponse } from '../models/PreSignedUrlResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ImageService {
    /**
     * Get Image For Batch
     * @param batchId
     * @returns PreSignedUrlResponse Successful Response
     * @throws ApiError
     */
    public static getImageForBatch(
        batchId: number,
    ): CancelablePromise<PreSignedUrlResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/image',
            query: {
                'batch_id': batchId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
