/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

import * as React from "react";
import { GridProps, TextFieldProps } from "@aws-amplify/ui-react";
export declare type EscapeHatchProps = {
    [elementHierarchy: string]: Record<string, unknown>;
} | null;
export declare type VariantValues = {
    [key: string]: string;
};
export declare type Variant = {
    variantValues: VariantValues;
    overrides: EscapeHatchProps;
};
export declare type ValidationResponse = {
    hasError: boolean;
    errorMessage?: string;
};
export declare type ValidationFunction<T> = (value: T, validationResponse: ValidationResponse) => ValidationResponse | Promise<ValidationResponse>;
export declare type ResultUpdateFormInputValues = {
    id?: string;
    createdAt?: string;
    updatedAt?: string;
    result?: string;
};
export declare type ResultUpdateFormValidationValues = {
    id?: ValidationFunction<string>;
    createdAt?: ValidationFunction<string>;
    updatedAt?: ValidationFunction<string>;
    result?: ValidationFunction<string>;
};
export declare type PrimitiveOverrideProps<T> = Partial<T> & React.DOMAttributes<HTMLDivElement>;
export declare type ResultUpdateFormOverridesProps = {
    ResultUpdateFormGrid?: PrimitiveOverrideProps<GridProps>;
    id?: PrimitiveOverrideProps<TextFieldProps>;
    createdAt?: PrimitiveOverrideProps<TextFieldProps>;
    updatedAt?: PrimitiveOverrideProps<TextFieldProps>;
    result?: PrimitiveOverrideProps<TextFieldProps>;
} & EscapeHatchProps;
export declare type ResultUpdateFormProps = React.PropsWithChildren<{
    overrides?: ResultUpdateFormOverridesProps | undefined | null;
} & {
    id?: string;
    result?: any;
    onSubmit?: (fields: ResultUpdateFormInputValues) => ResultUpdateFormInputValues;
    onSuccess?: (fields: ResultUpdateFormInputValues) => void;
    onError?: (fields: ResultUpdateFormInputValues, errorMessage: string) => void;
    onChange?: (fields: ResultUpdateFormInputValues) => ResultUpdateFormInputValues;
    onValidate?: ResultUpdateFormValidationValues;
} & React.CSSProperties>;
export default function ResultUpdateForm(props: ResultUpdateFormProps): React.ReactElement;
